"""Registration form for the participants."""

from wtforms import (
    EmailField,
    Form,
    RadioField,
    StringField,
    SubmitField,
    TextAreaField,
    validators,
)


def _strip_or_none(value: str | None) -> str | None:
    if value is not None:
        value = value.strip()

    return value if value else None


def filter_empty_string_to_none():
    return [
        _strip_or_none,
    ]


class RegistrationForm(Form):
    """Registration form for participants.

    Validator constraints have to be manually synchronized with:
    - `registration_app/db/migrations` to match the database schema
    """

    full_name = StringField(
        "Full Name",
        [
            validators.InputRequired(),
            validators.Length(max=512),
        ],
    )
    affiliation = StringField(
        "Affiliation",
        [
            validators.Length(max=256),
        ],
        filters=filter_empty_string_to_none(),
    )
    email = EmailField(
        "Email address",
        [
            validators.InputRequired(),
            validators.Length(max=512),
        ],
    )

    invoicing_address_line_1 = StringField(
        "Address Line 1",
        [
            validators.InputRequired(),
            validators.Length(max=256),
        ],
    )
    invoicing_address_line_2 = StringField(
        "Address Line 2",
        [
            validators.Length(max=256),
        ],
    )
    invoicing_address_city = StringField(
        "City",
        [
            validators.Length(max=256),
        ],
    )
    invoicing_address_country = StringField(
        "Country",
        [
            validators.InputRequired(),
            validators.Length(max=256),
        ],
    )
    invoicing_address_zip_code = StringField(
        "ZIP Code",
        [
            validators.Length(max=64),
        ],
    )
    invoicing_vat_number = StringField(
        "VAT Number",
        [
            validators.Length(max=64),
        ],
    )

    registration_type = RadioField(
        "Registration type",
        [
            validators.InputRequired(),
        ],
        choices=[
            ("REGULAR", "Regular"),
            ("STUDENT", "Student"),
            ("ACCOMPANYING", "Accompanying"),
        ],
    )

    remarks = TextAreaField(
        "Remarks (including dietary restrictions, accessibility requirements, etc.)",
        [
            validators.Length(max=16384),
        ],
        filters=filter_empty_string_to_none(),
    )

    photo_consent = RadioField(
        "Do you consent with us taking your photos?",
        [
            validators.InputRequired(),
        ],
        choices=[
            ("YES", "Yes, I give my consent"),
            ("NO", "No, I do not give my consent"),
        ],
    )

    submit = SubmitField("Register and proceed to payment")
