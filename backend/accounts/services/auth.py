import logging
from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException

from accounts.models import User
# adjust these two import paths to your project
from accounts.tokenization import create_access_token, create_refresh_token
# from notifications.factory import NotificationFactory
from captcha.services import CaptchaService
from accounts.exceptions import (
    TokenAlreadyBlacklisted,
    LoginError,
    InvalidCredentials,
    AccountInactive,
    AccountLocked,
    OutsideAllowedTime,
    IPNotAllowed,
    InvalidCaptcha,
)

logger = logging.getLogger(__name__)
_DUMMY_HASH = make_password("dummy-password-for-timing")


# ── services ────────────────────────────────────────────────────────────
@dataclass
class LoginResult:
    user: User
    access_token: str
    refresh_token: str


def verify_captcha(captcha_id: str, captcha_answer: str) -> None:
    ok, message = CaptchaService.validate_captcha(key=captcha_id, user_response=captcha_answer)
    if not ok:
        raise InvalidCaptcha(detail=message)


def _locked_minutes(user: User) -> int:
    return int((user.locked_until - timezone.now()).total_seconds() // 60) + 1


def ensure_can_login(user: User, client_ip: str) -> None:
    """Account-state checks shared by password login and SSO."""
    if not user.is_active:
        raise AccountInactive()
    if user.is_locked_out():
        raise AccountLocked(_locked_minutes(user))
    if not user.is_superuser and not user.has_time_based_access():
        raise OutsideAllowedTime()
    if not user.is_ip_allowed(client_ip):
        raise IPNotAllowed()


def _register_failed_attempt(user: User) -> None:
    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=user.pk)  # no lost counts
        user.user_attempt_login_limit += 1
        fields = ["user_attempt_login_limit"]

        if user.user_attempt_login_limit >= settings.USER_LOGIN_ATTEMPTS_DEACTIVATE_LIMIT:
            user.is_active = False
            fields.append("is_active")
        elif user.user_attempt_login_limit % settings.USER_LOGIN_ATTEMPTS_LOCK_LIMIT == 0:
            user.locked_until = timezone.now() + timedelta(hours=2)
            fields.append("locked_until")

        user.save(update_fields=fields)


def authenticate_with_password(username: str, password: str, client_ip: str) -> User:
    user = User.objects.filter(username=username).first()

    if user is None:
        check_password(password, _DUMMY_HASH)  # same cost as a real check
        raise InvalidCredentials()

    # Lock must be checked BEFORE the password, otherwise locking is useless
    if user.is_locked_out():
        raise AccountLocked(_locked_minutes(user))

    if not user.check_password(password):
        _register_failed_attempt(user)
        raise InvalidCredentials()

    # Only someone with the correct password learns about disabled/IP/time restrictions
    ensure_can_login(user, client_ip)
    return user


def complete_login(user: User, client_ip: str) -> LoginResult:
    with transaction.atomic():
        user.previous_last_login = user.last_login
        user.last_login = timezone.now()
        user.user_attempt_login_limit = 0
        user.locked_until = None
        user.last_ip_login = client_ip
        user.save(update_fields=[
            "last_login", "previous_last_login", "locked_until",
            "user_attempt_login_limit", "last_ip_login",
        ])

    access = create_access_token(
        user_id=user.id, expires_in_seconds=settings.JWT_ACCESS_TOKEN_EXPIRE_IN_SECOND)
    refresh = create_refresh_token(
        user_id=user.id, expires_in_days=settings.JWT_REFRESH_TOKEN_EXPIRE_IN_DAYS)

    # A notification failure must never break a successful login
    # try:
    #     NotificationFactory.for_everytime_user_login(targetuser=user)
    # except Exception:
    #     logger.exception("login notification failed for user %s", user.pk)

    return LoginResult(user=user, access_token=access, refresh_token=refresh)


def set_refresh_cookie(response, refresh_token: str, remember_me: bool) -> None:
    max_age = int(timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_IN_DAYS).total_seconds()) if remember_me else None
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
        max_age=max_age,
    )