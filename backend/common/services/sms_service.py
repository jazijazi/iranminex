import uuid
import logging
from dataclasses import dataclass, field
from typing import Optional

import requests
from decouple import config
from django.conf import settings

# Loggers
database_logger = logging.getLogger("custom_database_loger")
file_logger = logging.getLogger("custom_file_loger")
sms_file_logger = logging.getLogger("sms_file_logger")

# Constants
SMS_API_URL = "https://ws.adpdigital.com/url/send"
SMS_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}


# ── Session ────────────────────────────────────────────────────────────────────

def _build_session() -> requests.Session:
    s = requests.Session()
    s.trust_env = False
    # s.proxies = {"http": "", "https": "", "socks": ""}
    return s


session = _build_session()


# ── Data ───────────────────────────────────────────────────────────────────────

@dataclass
class SMSPayload:
    """Represents a structured payload ready to be sent to the SMS gateway."""

    phones: list[str]
    text: str
    client_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.client_ids = [str(uuid.uuid4()).split("-")[-1] for _ in self.phones]

    def to_request_data(self) -> dict:
        return {
            "username": config("SMSUSER", default="smsuser"),
            "password": config("SMSPASS", default="smspassword"),
            "dstaddress": ",".join(self.phones),
            "clientid": ",".join(self.client_ids),
            "unicode": 1,
            "body": self.text,
            # "srcaddress": "982000334455",  # uncomment to set a sender number
        }


# ── Validation ─────────────────────────────────────────────────────────────────

def _validate_sms_inputs(phones: list[str], text: str) -> None:
    if not isinstance(phones, list):
        raise TypeError("'phones' must be a list.")
    if not phones:
        raise ValueError("'phones' must contain at least one number.")
    if not text or not text.strip():
        raise ValueError("'text' cannot be empty.")


# ── Core logic ─────────────────────────────────────────────────────────────────

def _send_to_gateway(payload: SMSPayload) -> None:
    """POST the payload to the SMS gateway and handle the response."""
    phones_label = ", ".join(payload.phones)

    try:
        response = session.post(
            SMS_API_URL,
            data=payload.to_request_data(),
            headers=SMS_HEADERS,
            timeout=(20, 70),
        )
        _handle_gateway_response(response, payload)
    except requests.exceptions.RequestException as exc:
        sms_file_logger.critical(
            "SMS send failed for %s — exception: %s", phones_label, exc
        )
        raise


def _handle_gateway_response(response: requests.Response, payload: SMSPayload) -> None:
    """Interpret the gateway response and log accordingly.

    NOTE: The gateway always returns HTTP 200; errors are signalled by a
    response body that starts with ``"ERR:"``.
    """
    phones_label = ", ".join(payload.phones)
    is_success = (
        response.status_code == 200
        and response.text
        and not response.text.startswith("ERR:")
    )

    if is_success:
        msg = f"پیامک به {phones_label} با نتیجه {response.text} ارسال شد"
        file_logger.info(msg)
        database_logger.info(msg)
        sms_file_logger.info(
            "SMS sent successfully to %s | text: %s", phones_label, payload.text
        )
    else:
        msg = f"ارسال پیامک به {phones_label} ناموفق بود — پاسخ: {response.text}"
        file_logger.error(msg)
        database_logger.error(msg)
        sms_file_logger.error(
            "SMS failed for %s | text: %s | response: %s",
            phones_label,
            payload.text,
            response.text,
        )
        raise requests.exceptions.RequestException(
            f"Gateway error (HTTP {response.status_code}): {response.text}"
        )


def _log_debug_send(payload: SMSPayload) -> None:
    """Print a summary instead of hitting the real gateway in DEBUG mode."""
    separator = "-" * 40
    sms_file_logger.debug("SMS skipped (DEBUG mode) for %s", ", ".join(payload.phones))
    lines = [
        separator,
        "SEND SMS CALLED IN DEBUG ENV",
        *[f"  clientid: {cid}  →  phone: {phone}" for cid, phone in zip(payload.client_ids, payload.phones)],
        f"  text: {payload.text}",
        separator,
    ]
    print("\n".join(lines))


# ── Public API ─────────────────────────────────────────────────────────────────

def send_sms(phones: list[str], text: str, sender: Optional[str] = None) -> None:
    """Send an SMS to one or more phone numbers.

    Args:
        phones: List of destination phone numbers.
        text:   Message body.
        sender: Optional sender number (overrides the gateway default).

    Raises:
        TypeError:  If *phones* is not a list.
        ValueError: If *phones* is empty or *text* is blank.
        requests.exceptions.RequestException: If the gateway returns an error.
    """
    _validate_sms_inputs(phones, text)

    sms_file_logger.info(
        "Attempting SMS to %s | text: %s", ", ".join(phones), text
    )

    payload = SMSPayload(phones=phones, text=text)

    if settings.DEBUG:
        _log_debug_send(payload)
    else:
        _send_to_gateway(payload)