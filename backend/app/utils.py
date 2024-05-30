import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import emails  # type: ignore
from jinja2 import Template
from jose import JWTError, jwt

from app.core.config import settings


@dataclass
class EmailData:
    html_content: str
    subject: str


def render_email_template(*, template_name: str, context: dict[str, Any]) -> str:
    template_str = (
        Path(__file__).parent / "email-templates" / "build" / template_name
    ).read_text()
    html_content = Template(template_str).render(context)
    return html_content


def send_email(
    *,
    email_to: str,
    subject: str = "",
    html_content: str = "",
) -> None:
    assert settings.emails_enabled, "no provided configuration for email variables"
    message = emails.Message(
        subject=subject,
        html=html_content,
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    elif settings.SMTP_SSL:
        smtp_options["ssl"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, smtp=smtp_options)
    logging.info(f"send email result: {response}")

    return response


def generate_test_email(email_to: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    html_content = render_email_template(
        template_name="test_email.html",
        context={"project_name": settings.PROJECT_NAME, "email": email_to},
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    link = f"{settings.server_host}/reset-password?token={token}"
    html_content = render_email_template(
        template_name="reset_password.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_new_account_email(
    email_to: str, username: str, password: str
) -> EmailData:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    html_content = render_email_template(
        template_name="new_account.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": settings.server_host,
        },
    )
    return EmailData(html_content=html_content, subject=subject)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.now
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return str(decoded_token["sub"])
    except JWTError:
        return None


def send_signature_request_email(
    email_to: str, link: str, document_title: str, message: str
) -> emails.Message:
    subject = f"Signature Request for {document_title}"
    html_content = f"""<p>You have a new signature request.</p>
                        <p>Message: {message}</p>
                        <p>Please <a href='{link}'>click here</a> to sign the document.</p>"""
    return send_email(email_to=email_to, subject=subject, html_content=html_content)


def send_signature_request_notification_email(
    email_to: str, signature_request_name: str, signature_request_id: str, status: str
) -> emails.Message:
    subject = f"""Signature Request Status Update for '{signature_request_name}' \
                  whith id: '{signature_request_id}' \
                  """

    # Mapping status to user-friendly messages
    status_messages = {
        "draft": "The document is still in draft mode and hasn't been sent.",
        "sent": "The document has been sent out for signatures.",
        "completed": "All required parties have signed the document, and the process is now completed.",
        "expired": "The signature request has expired without being completed.",
        "canceled": "The signature request has been canceled."
    }

    # Generate a more detailed message based on the status
    detailed_message = status_messages.get(status, "There has been an update to your document.")

    # HTML content enhanced for better readability and formatting
    html_content = f"""
    <html>
        <head></head>
        <body>
            <p>Hello,</p>
            <p>This is a notification regarding the signature request for the document
            titled <strong>'{signature_request_name}'</strong>.</p>
            <p><strong>Status:</strong> {status.capitalize()}</p>
            <p><strong>Details:</strong> {detailed_message}</p>
            <p>
            If you have any questions or require further assistance, please do not hesitate to contact us.
            </p>
            <p>Thank you for using our services!</p>
        </body>
    </html>
    """

    return send_email(email_to=email_to, subject=subject, html_content=html_content)
