import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.core.config import settings

logger = logging.getLogger(__name__)


def send_password_reset_email(to_email: str, reset_url: str) -> None:
    """
    Sends a password reset email using SendGrid.
    Returns True if the email was submitted to SendGrid, False otherwise.
    """
    message = Mail(
        from_email=(settings.EMAIL_FROM, settings.EMAIL_FROM_NAME),
        to_emails=to_email,
        subject="Reset your password",
        html_content=(
            f"<p>We received a request to reset your password.</p>"
            f"<p><a href=\"{reset_url}\">Reset your password</a></p>"
            f"<p>If you didn't request this, you can ignore this email.</p>"
        ),
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            logger.info(
                "Reset email submitted to SendGrid",
                extra={"status_code": response.status_code},
            )
            return True
        logger.error(
            "SendGrid responded with non-2xx",
            extra={
                "status_code": response.status_code,
                "body": response.body,
                "headers": dict(response.headers),
            },
        )
        return False
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to send reset email: %s", exc)
        return False
