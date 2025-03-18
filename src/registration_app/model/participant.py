"""Model class for participant."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from registration_app.forms.registration import RegistrationForm


class RegistrationFeeType(Enum):
    """Participant registration fee types.

    There are three types of fees:
    - full fee
    - discounted fee (for ACM or IEEE members)
    - student fee
    """

    FULL = auto()
    DISCOUNTED = auto()
    STUDENT = auto()


@dataclass
class ParticipantInfo:
    """Information a participant provides us in the registration form."""

    postal_mail_opt_out: bool
    email_opt_in: bool

    full_name: str
    affiliation: str | None
    email: str

    acm_membership_number: str | None
    ieee_membership_number: str | None
    is_student: bool

    remarks: str | None

    @classmethod
    def from_form(cls, participant: RegistrationForm) -> "ParticipantInfo":
        """Creates a `ParticipantInfo` from `RegistrationForm` input."""

        return cls(
            postal_mail_opt_out=participant.privacy_policy_postal_mail_opt_out.data,
            email_opt_in=participant.privacy_policy_email_opt_in.data == "yes",
            full_name=participant.full_name.data,
            affiliation=participant.affiliation.data,
            email=participant.email.data,
            acm_membership_number=participant.acm_membership_number.data,
            ieee_membership_number=participant.ieee_membership_number.data,
            is_student=participant.is_student.data,
            remarks=participant.remarks.data,
        )


@dataclass
class Participant(ParticipantInfo):
    id: int
    date_registered: datetime
    fee_type: RegistrationFeeType
