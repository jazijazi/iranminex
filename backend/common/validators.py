import os
import magic
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^989\d{9}$',
    message="شماره تماس باید با 989 شروع شود و دقیقاً 12 رقم باشد.",
)

def codemeli_validator(value):
    if not value or len(value) != 10 or not value.isdigit() or len(set(value)) == 1:
        raise ValidationError("تعداد ارقام کد ملی اشتباه است.")

    digits = [int(c) for c in value]
    s = sum(d * (10 - i) for i, d in enumerate(digits[:9]))
    r = s % 11
    check = digits[9]

    if not ((r < 2 and check == r) or (r >= 2 and check == 11 - r)):
        raise ValidationError("کد ملی نامعتبر است.")

def validate_file_extension(value):
    """Check the filename extension against the allowed whitelist."""
    ext = os.path.splitext(value.name)[1].lower()
    allowed = getattr(settings, 'UPLOAD_ALLOWED_TYPES', {})
    if ext not in allowed:
        raise ValidationError(
            f"پسوند فایل مجاز نیست. پسوندهای مجاز: {', '.join(allowed.keys())}"
        )


def validate_file_content_type(value):
    """
    Sniff the file's real content via magic bytes and confirm it matches
    what its extension claims to be. Rejects renamed/spoofed files
    (e.g. a .exe renamed to .pdf, or an .html file renamed to .jpg).
    """
    allowed = getattr(settings, 'UPLOAD_ALLOWED_TYPES', {})
    ext = os.path.splitext(value.name)[1].lower()

    # extension check runs first; if it already failed, no point continuing
    expected_mimes = allowed.get(ext)
    if expected_mimes is None:
        raise ValidationError("پسوند فایل مجاز نیست")

    try:
        current_pos = value.tell()
        header = value.read(2048)
        value.seek(current_pos)  # always restore the stream position
    except Exception:
        raise ValidationError("خطا در خواندن فایل")

    if not header:
        raise ValidationError("فایل خالی است")

    try:
        detected_mime = magic.from_buffer(header, mime=True)
    except Exception:
        # fail closed: if we can't verify the file's real type, reject it
        raise ValidationError("امکان بررسی نوع فایل وجود ندارد")

    if detected_mime not in expected_mimes:
        raise ValidationError(
            f"محتوای فایل با پسوند آن مطابقت ندارد (نوع شناسایی‌شده: {detected_mime})"
        )


def validate_upload_file(value):
    """Convenience wrapper: run both checks together."""
    validate_file_extension(value)
    validate_file_content_type(value)