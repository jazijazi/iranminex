import logging

from django.db.models import Q

from common.services.sms_service import send_sms

from accounts.models import User
from contracts.models.SharhKhadamats import ShrhLayer

sms_file_logger = logging.getLogger("sms_file_logger")

# ── Constants ──────────────────────────────────────────────────────────────────

UNKNOWN = "نا مشخص"

# ── Helpers ────────────────────────────────────────────────────────────────────

def _safe(value: object, fallback: str = UNKNOWN) -> str:
    """Return ``str(value)`` when *value* is non-empty, otherwise *fallback*."""
    try:
        text = str(value).strip() if value is not None else ""
        return text if text else fallback
    except Exception:
        return fallback


def _safe_chain(*getters, fallback: str = UNKNOWN) -> str:
    """
    Try each zero-argument callable in order; return the first non-empty result.
    Falls back to *fallback* if every callable raises or returns empty.

    Usage:
        _safe_chain(lambda: obj.a.b.c, lambda: obj.a.b.d)
    """
    for getter in getters:
        try:
            result = str(getter()).strip()
            if result:
                return result
        except Exception:
            continue
    return fallback


# ── Factory ────────────────────────────────────────────────────────────────────

class SMSFactory:
    """
    Central factory for composing and dispatching domain-specific SMS messages.

    Add one ``send_*`` class-method per notification type; keep all
    text-building and recipient-resolution logic private.
    """

    # ── Recipient resolution ───────────────────────────────────────────────────

    @staticmethod
    def _get_mojri_phones(shrhlayer: ShrhLayer, uploader_user: User) -> list[str]:
        try:
            phones: list[str] = list(
                shrhlayer.accessible_by_users
                .filter(Q(roles__title="مجری") | Q(is_controller=True))
                .exclude(id=uploader_user.id)
                .exclude(phonenumber__isnull=True)
                .exclude(phonenumber="")
                .values_list("phonenumber", flat=True)
                .distinct()
            )
            return phones
        except Exception as exc:
            sms_file_logger.error("Failed to resolve مجری phone list — %s", exc)
            return []

    # ── Text builders ──────────────────────────────────────────────────────────

    @staticmethod
    def _build_layeradd_text(uploader_user: User, shrhlayer: ShrhLayer) -> str:
        """
        Compose the layer-upload notification text.

        Every field is accessed through ``_safe_chain`` so a missing / None
        value never raises; it silently becomes ``UNKNOWN`` (نا مشخص).
        """
        layername_fa = _safe_chain(
            lambda: shrhlayer.layer_name.layername_fa,
        )

        contract_title = _safe_chain(
            lambda: shrhlayer.shrh_base.contract.title,
        )

        contract_number = _safe_chain(
            lambda: shrhlayer.shrh_base.contract.number,
        )

        uploader_name = _safe_chain(
            lambda: uploader_user.get_full_name_fa(),           # custom method (preferred)
            lambda: f"{uploader_user.first_name_fa} {uploader_user.last_name_fa}",
            lambda: uploader_user.get_full_name(),              # Django built-in fallback
            lambda: uploader_user.username,                     # last resort
        )

        return (
            f"لایه {layername_fa} "
            f"از قرارداد {contract_title} ({contract_number}) "
            f"توسط کاربر {uploader_name} "
            f"با موفقیت بارگذاری شد"
        )

    # ── Public API ─────────────────────────────────────────────────────────────

    @classmethod
    def send_layeradd_sms_to_mojries(
        cls,
        uploader_user: User,
        shrhlayer: ShrhLayer,
    ) -> None:
        """
        Notify all مجری / controller users that a new layer has been uploaded.

        Args:
            uploader_user: The ``User`` who performed the upload.
            shrhlayer:     The ``ShrhLayer`` that was just added.

        This method is intentionally exception-safe: any failure is logged and
        swallowed so that the caller's workflow is never interrupted.
        """
        try:
            phones = cls._get_mojri_phones(shrhlayer, uploader_user)

            if not phones:
                sms_file_logger.warning(
                    "send_layeradd_sms_to_mojries: no مجری phones found "
                    "(layer pk=%s, uploader pk=%s)",
                    _safe(getattr(shrhlayer, "pk", None)),
                    _safe(getattr(uploader_user, "pk", None)),
                )
                return

            text = cls._build_layeradd_text(uploader_user, shrhlayer)

            sms_file_logger.info(
                "send_layeradd_sms_to_mojries: dispatching to %d recipient(s) "
                "(layer pk=%s)",
                len(phones),
                _safe(getattr(shrhlayer, "pk", None)),
            )

            send_sms(phones=phones, text=text)

        except Exception as exc:
            sms_file_logger.error(
                "send_layeradd_sms_to_mojries: unexpected error — %s", exc
            )