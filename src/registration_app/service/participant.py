"""Service for participants."""

import logging
from dataclasses import dataclass, field

from registration_app.app import app
from registration_app.db.participant import add_participant
from registration_app.forms.registration import RegistrationForm
from registration_app.model.participant import ParticipantInfo, ParticipantType
from registration_app.service.emailer import EmailTemplate, Emailer

import psycopg
import psycopg.errors
from bottle import abort


logger = logging.getLogger(__name__)


@dataclass
class ParticipantRegistrationResult:
    """Returned by `register_participant`.

    Attributes:
        errors: List of errors messages that should be displayed to the user. If this
            list is not empty, then something went wrong during the registration.
    """

    errors: list[str] = field(default_factory=list)

    def compute_fee(self) -> int:
        """Computes the fee price from `self.fee_type`."""
        return 0
        # return compute_price_in_czk(self.fee_type)


def register_participant(
    participant_input: RegistrationForm,
) -> ParticipantRegistrationResult:
    """Registers a participant based on form input."""
    res = ParticipantRegistrationResult()
    try:
        participant_type = determine_participant_type(participant_input)
    except ValueError:
        logger.exception(
            f"Participant with email '{participant_input.email.data}' entered invalid"
            " registration type"
        )
        err_msg = (
            f"Invalid value for registration type ('{participant_input.email.data}')"
        )
        abort(400, err_msg)
        res.errors.append(err_msg)
        return res
    participant_info = ParticipantInfo.from_form(
        participant_input,
        participant_type,
    )
    try:
        add_participant(participant_info)
    except psycopg.Error:
        logger.exception(
            f"Could not register participant with email '{participant_input.email}'",
        )
        res.errors.append(
            "An unexpected error has occurred when registering you. Please contact us"
            " at the email address below."
        )
        return res

    # TODO(Tung): Initialize once throughout the app.
    emailer = Emailer(
        app.config["registration_app.Email.server"],
        app.config["registration_app.Email.from"],
        app.config["registration_app.Email.content.subject_prefix"],
        app.config["registration_app.Email.cc"],
        app.config["registration_app.Email.enabled"],
    )

    emailer.send_email_from_template(
        participant_info.email,
        participant_info.full_name,
        EmailTemplate.REGISTRATION,
        {
            "payment_link": "not-yet-implemented",
        },
    )

    return res


def determine_participant_type(form: RegistrationForm) -> ParticipantType:
    """Determines `ParticipantType` from `RegistrationForm` input."""
    return ParticipantType(form.registration_type.data)
