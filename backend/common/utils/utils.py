from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import (
    ValidationError,
    NotAuthenticated,
    Throttled,
)
from common.exceptions import (
    GeoFrameValidationError,
)
from django.db.models import ProtectedError


def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response({'detail': 'توکن ارائه نشده است یا کاربر وارد نشده است'}, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, Throttled):
        wait = exc.wait
        minutes = round(wait / 60) if wait else 1
        custom_response_data = {
            "detail": f"تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً حدود {minutes} دقیقه دیگر تلاش کنید."
        }
        return Response(custom_response_data, status=status.HTTP_429_TOO_MANY_REQUESTS)

    if isinstance(exc, GeoFrameValidationError):
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    # خطای full_clean مدل‌ها (Django ValidationError) -> 400 با همان قالب خطای DRF
    if isinstance(exc, DjangoValidationError):
        exc = ValidationError(exc.message_dict if hasattr(exc, "error_dict") else exc.messages)

    # حذف رکوردی که رکوردهای دیگر با on_delete=PROTECT به آن وابسته‌اند
    elif isinstance(exc, ProtectedError):
        exc = ValidationError({"detail": "این رکورد به رکوردهای دیگر وابسته است و قابل حذف نیست"})

    # fallback to default handler
    return exception_handler(exc, context)