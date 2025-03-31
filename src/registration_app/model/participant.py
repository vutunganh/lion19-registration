"""Model class for participant."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from registration_app.forms.registration import RegistrationForm


class ParticipantType(str, Enum):
    """Participant fee types.

    Mainly used for determining the fee type.
    """

    REGULAR = "REGULAR"
    STUDENT = "STUDENT"
    ACCOMPANYING = "ACCOMPANYING"


@dataclass
class ParticipantInfo:
    """Information a participant provides us in the registration form."""

    full_name: str
    affiliation: str | None
    email: str

    invoicing_address_line_1: str
    invoicing_address_line_2: str | None
    invoicing_address_city: str | None
    invoicing_address_country: str
    invoicing_address_zip_code: str | None
    invoicing_vat_number: str | None

    participant_type: ParticipantType

    remarks: str | None

    @classmethod
    def from_form(
        cls,
        participant: RegistrationForm,
        participant_type: ParticipantType,
    ) -> "ParticipantInfo":
        """Creates a `ParticipantInfo` from `RegistrationForm` input."""

        return cls(
            full_name=participant.full_name.data,  # pyright: ignore
            affiliation=participant.affiliation.data,
            email=participant.email.data,  # pyright: ignore
            invoicing_address_line_1=participant.invoicing_address_line_1.data,  # pyright: ignore
            invoicing_address_line_2=participant.invoicing_address_line_2.data,
            invoicing_address_city=participant.invoicing_address_city.data,
            invoicing_address_country=participant.invoicing_address_country.data,  # pyright: ignore
            invoicing_address_zip_code=participant.invoicing_address_zip_code.data,
            invoicing_vat_number=participant.invoicing_vat_number.data,
            participant_type=participant_type,
            remarks=participant.remarks.data,
        )


@dataclass
class Participant(ParticipantInfo):
    id: int
    date_registered: datetime
    has_paid: bool
