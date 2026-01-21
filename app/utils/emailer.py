from __future__ import annotations

import asyncio
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Optional
from app.utils.structlog_config import logger

from app.core.config import settings

log = logger.bind(module=__name__, service="emailer")


@dataclass(frozen=True)
class EmailPayload:
    to: str
    subject: str
    body_text: str
    body_html: Optional[str] = None


class EmailSendError(RuntimeError):
    pass


def _build_message(payload: EmailPayload, *, from_email: str) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = from_email
    msg["To"] = payload.to
    msg["Subject"] = payload.subject

    msg.set_content(payload.body_text)
    if payload.body_html:
        msg.add_alternative(payload.body_html, subtype="html")

    return msg


async def _smtp_send_message(
    msg: EmailMessage,
    *,
    host: str,
    port: int,
    username: Optional[str],
    password: Optional[str],
    use_tls: bool,
    start_tls: bool,
    timeout: float,
) -> None:
    import aiosmtplib

    await aiosmtplib.send(
        msg,
        hostname=host,
        port=port,
        username=username,
        password=password,
        use_tls=use_tls,
        start_tls=start_tls,
        timeout=timeout,
    )


async def send_email(
    *,
    to: str,
    subject: str,
    body: str,
    html: Optional[str] = None,
    raise_on_error: bool = False,
) -> None:
    """
    Production behavior:
      - Uses SMTP if configured.
      - Retries on transient failures.
      - By default does NOT crash user request if email fails (raise_on_error=False).
    """

    payload = EmailPayload(to=to, subject=subject, body_text=body, body_html=html)
    msg = _build_message(payload, from_email=settings.smtp.sender_email)

    last_exc: Optional[Exception] = None
    for attempt in range(1, settings.smtp.retries + 1):
        try:
            await _smtp_send_message(
                msg,
                host=settings.smtp.host,
                port=settings.smtp.port,
                username=settings.smtp.username,
                password=settings.smtp.password,
                use_tls=settings.smtp.use_tls,
                start_tls=settings.smtp.start_tls,
                timeout=settings.smtp.timeout,
            )
            log.info("Email sent. subject=%s to=%s", subject, to)
            return
        except Exception as e:
            last_exc = e
            log.warning(
                "Email send failed (attempt %d/%d). subject=%s to=%s err=%r",
                attempt,
                settings.smtp.retries,
                subject,
                to,
                e,
            )
            if attempt < settings.smtp.retries:
                await asyncio.sleep(settings.smtp.base_backoff * (2 ** (attempt - 1)))

    if raise_on_error:
        raise EmailSendError(
            f"Email send failed to={to} subject={subject}"
        ) from last_exc

    log.error(
        "Email окончательно не отправлено. subject=%s to=%s. Ошибка подавлена (raise_on_error=False).",
        subject,
        to,
    )
