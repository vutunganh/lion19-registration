"""Service for emails."""

import importlib.resources as resources
import logging
import string
from dataclasses import dataclass, field
from email.message import EmailMessage
from enum import Enum
from smtplib import SMTP_SSL

from registration_app import APP_NAME
from registration_app.app import app

logger = logging.getLogger(__name__)


class EmailTemplate(str, Enum):
    REGISTRATION = "REGISTRATION"
    REGISTRATION_WITHOUT_PAYMENT_LINK = "REGISTRATION_WITHOUT_PAYMENT_LINK"
    RECEIPT = "RECEIPT"

template_map: dict[EmailTemplate, str] = {
    EmailTemplate.REGISTRATION: 'registration-confirmation.txt',
    EmailTemplate.REGISTRATION_WITHOUT_PAYMENT_LINK: 'registration-confirmation-without-payment.txt',
    EmailTemplate.RECEIPT: 'receipt.txt',
}

subject_map: dict[EmailTemplate, str] = {
    EmailTemplate.REGISTRATION: 'Registration confirmation',
    EmailTemplate.RECEIPT: 'Registration fee receipt',
}


@dataclass
class Emailer:
    """
    Email utilities.
    """
    server: str
    from_addr: str
    subj_prefix: str
    cc: list[str] = field(default_factory=list)
    enabled: bool = False

    def send_email_from_template(
        self,
        to_addr: str,
        full_name: str,
        template_type: EmailTemplate,
        subst: dict[str, str],
    ):
        email_body = self.read_template(
            to_addr,
            f'{self.subj_prefix} {subject_map[template_type]}',
            full_name,
            subst,
            template_type,
        )

        self.send_email(email_body)

    def send_email(self, mail: EmailMessage):
        if not self.enabled:
            return

        try:
            smtp = SMTP_SSL(self.server)
            smtp.send_message(mail)
        except Exception:
            logger.exception(f"Could not send email to {mail['To']}")

    def read_template(
            self,
            to_addr: str,
            subject: str,
            full_name: str,
            subst: dict[str, str],
            template_type: EmailTemplate,
    ) -> EmailMessage:
        msg = EmailMessage()
        with resources.path(APP_NAME, "email_templates") as p:
            with (p / template_map[template_type]).open() as f:
                template = string.Template(f.read())
        msg_content = template.template
        try:
            msg_content = template.substitute({'full_name': full_name } | subst)
        except (KeyError, ValueError):
            logger.warn(
                f'Message "{template_type}" to <{to_addr}> was not fully substituted',
            )

        msg.set_content(msg_content)
        msg['Subject'] = subject
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        return msg
