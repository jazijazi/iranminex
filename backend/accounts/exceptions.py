from rest_framework.exceptions import AuthenticationFailed, ValidationError

class TokenAlreadyBlacklisted(Exception):
    """Raised by TokenBlacklistService.blacklist when the jti is already blocked."""

class LoginError(AuthenticationFailed):
    """Base: any reason a login is refused (401)."""
    default_code = "login_failed"


class InvalidCredentials(LoginError):
    default_detail = "نام کاربری یا رمز عبور اشتباه است"
    default_code = "invalid_credentials"

class AccountInactive(LoginError):
    default_detail = "اکانت شما موقتاً غیرفعال شده است لطفا با پشتیبانی تماس بگیرید"
    default_code = "account_inactive"

class AccountLocked(LoginError):
    default_code = "account_locked"
    def __init__(self, minutes: int):
        super().__init__(f"حساب شما موقتاً قفل شده است. لطفاً {minutes} دقیقه دیگر تلاش کنید")

class OutsideAllowedTime(LoginError):
    default_detail = "دسترسی شما در این بازه زمانی مجاز نیست"
    default_code = "outside_allowed_time"

class IPNotAllowed(LoginError):
    default_detail = "ورود از این آدرس IP مجاز نیست"
    default_code = "ip_not_allowed"

class InvalidCaptcha(ValidationError):
    default_code = "invalid_captcha"
    