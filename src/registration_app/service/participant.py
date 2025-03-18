"""Service for participants."""

import logging
from dataclasses import dataclass, field

from registration_app.app import app
from registration_app.db.participant import MembershipType, add_participant, is_membership_unused
from registration_app.forms.registration import RegistrationForm
from registration_app.model.participant import ParticipantInfo, RegistrationFeeType

import psycopg
import psycopg.errors

from registration_app.service.emailer import EmailTemplate, Emailer

logger = logging.getLogger(__name__)


@dataclass
class ParticipantRegistrationResult:
    """Returned by `register_participant`.

    Attributes:
        fee_type: What is the fee type of the participant.
        errors: List of errors messages that should be displayed to the user. If this
            list is not empty, then something went wrong during the registration.
    """

    fee_type: RegistrationFeeType = field(
        default=RegistrationFeeType.FULL,
    )
    warn_invalid_membership: bool = False
    errors: list[str] = field(default_factory=list)

    def compute_fee(self) -> int:
        """Computes the fee price from `self.fee_type`."""
        return compute_price_in_czk(self.fee_type)


def register_participant(
    participant_input: RegistrationForm,
) -> ParticipantRegistrationResult:
    """Registers a participant based on form input.
    
    Steps performed:
    1. Determine the payment amount.
        - If they are a student, just trust them and give them a discount.
        - If they provided an ACM membership number, check if it is applicable for a
          discount. It is not valid if the ACM membership number is not valid or if a
          discount has already been applied to this ACM membership number.
            - If not, then we want the participant to immediately redo the form without
                saving any of the information they provided.
        - We have decided that in case of a garbage value, we still give participants a
          discount. We shall run on a honor-based system.
    2. Inserts the participant into the database.
    3. Send the participant a notification email.

    TODOs:
        - We will need to redirect the participant to the right URL for paying.
    """
    res = ParticipantRegistrationResult()
    participant_info = ParticipantInfo.from_form(participant_input)


    try:
        add_participant(participant_info, res.fee_type)
    except psycopg.Error:
        logger.exception(
            f"Could not register participant with email '{participant_input.email}'",
        )
        res.errors.append(
            "An unexpected error has occurred when registering you. Please contact us"
            " at the email address below."
        )
        return res

    # TODO(Tung): Initialize once.
    emailer = Emailer(
        app.config["stoc_registration.Email.server"],
        app.config["stoc_registration.Email.from"],
        app.config["stoc_registration.Email.content.subject_prefix"],
        app.config["stoc_registration.Email.cc"],
        app.config["stoc_registration.Email.enabled"],
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


def compute_price_in_czk(fee_type: RegistrationFeeType) -> int:
    """Computes the fee in CZK from `ParticipantRegistrationFeeType`."""
    match fee_type:
        case RegistrationFeeType.FULL:
            res = app.config["stoc_registration.Payment.standard_price"]
        case RegistrationFeeType.DISCOUNTED:
            res = app.config["stoc_registration.Payment.discounted_price"]
        case RegistrationFeeType.STUDENT:
            res = app.config["stoc_registration.Payment.student_price"]
    return int(res)


def can_apply_ieee_membership(ieee_membership_number: str, email: str) -> bool:
    return is_membership_unused(MembershipType.IEEE, ieee_membership_number, email)
