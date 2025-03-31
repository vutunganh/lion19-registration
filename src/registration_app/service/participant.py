"""Service for participants."""

import logging
from dataclasses import dataclass, field
from datetime import datetime

from registration_app.app import app
from registration_app.db.participant import (
    add_participant,
    delete_participant_by_id,
    record_successful_payment,
)
from registration_app.forms.registration import RegistrationForm
from registration_app.model.participant import ParticipantInfo, ParticipantType
from registration_app.service.emailer import EmailTemplate, Emailer
from registration_app.service.payment import (
    PaymentGateException,
    PaymentUnsuccessfulException,
    handle_payment_callback,
    request_payment,
)

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
        payment_link: Link where the participant should pay the registration fee.
    """

    errors: list[str] = field(default_factory=list)
    payment_link: str | None = None

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
        res.errors.append(err_msg)
        abort(400, err_msg)
        # This line is unreachable but bottle doesn't have strong enough typing. So
        # we make a return here to help the type checker to know that in case of an
        # error in the try-block, no code will be executed.
        return res
    participant_info = ParticipantInfo.from_form(
        participant_input,
        participant_type,
    )
    try:
        id = add_participant(participant_info)
    except psycopg.Error:
        logger.exception(
            f"Could not register participant with email '{participant_input.email}'",
        )
        res.errors.append(
            "An unexpected error has occurred when registering you. Please contact us"
            " at the email address below."
        )
        return res

    payment_amount = determine_payment_amount(participant_type)
    if participant_info.email in [
        "hartman@iuuk.mff.cuni.cz",
        "tung@iuuk.mff.cuni.cz",
        "hladik@kam.mff.cuni.cz",
    ]:
        payment_amount = 1
    payment_amount *= int(
        app.config["registration_app.Payment.price.smallest_unit_multiplier"],
    )

    try:
        payment_link = request_payment(id, payment_amount)
    except PaymentGateException:
        logger.exception(
            f"Could not request payment link for '{participant_info.email}'",
        )
        res.errors.append(
            "We could not create a payment link for you."
            " This is most likely a one-time error so please try to submit the form"
            " again. In case of repeated errors, please contact us at the email below."
            " We apologize for the inconvenience."
        )
        try:
            delete_participant_by_id(id)
        except:  # noqa: E722
            pass  # ignore on purpose
        return res
    res.payment_link = payment_link

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
            "payment_link": payment_link,
        },
    )
    return res


@dataclass
class PaymentCallbackResult:
    """Result of handling payment callback."""

    errors: list[str] = field(default_factory=list)


def validate_payment(callback_url: str) -> PaymentCallbackResult:
    """Handles the callback from payment gate.

    Args:
        callback_url: The entire callback URL. So take `LocalRequest.url` and pass it
            here.
    """
    res = PaymentCallbackResult()
    try:
        id = handle_payment_callback(callback_url)
    except PaymentUnsuccessfulException as e:
        res.errors.append(e.err_msg)
        return res

    participant_info = record_successful_payment(id)

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
        EmailTemplate.RECEIPT,
        {
            "affiliation": participant_info.affiliation or "",
            "address_line_1": participant_info.invoicing_address_line_1,
            "address_line_2": participant_info.invoicing_address_line_2 or "",
            "city": participant_info.invoicing_address_city or "",
            "country": participant_info.invoicing_address_country,
            "zip_code": participant_info.invoicing_address_zip_code or "",
            "vat_number": participant_info.invoicing_vat_number or "",
            "price": str(determine_payment_amount(participant_info.participant_type)),
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
    )

    return res


def determine_payment_amount(p: ParticipantType) -> int:
    """Determine payment amount based on participant type."""
    match p:
        case ParticipantType.REGULAR:
            return app.config["registration_app.Payment.price.regular"]
        case ParticipantType.STUDENT:
            return app.config["registration_app.Payment.price.student"]
        case ParticipantType.ACCOMPANYING:
            return app.config["registration_app.Payment.price.accompanying"]


def determine_participant_type(form: RegistrationForm) -> ParticipantType:
    """Determines `ParticipantType` from `RegistrationForm` input."""
    return ParticipantType(form.registration_type.data)
