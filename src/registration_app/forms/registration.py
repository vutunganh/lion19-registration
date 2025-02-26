"""Registration form for the participants."""

from wtforms import (
    BooleanField,
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
    """Registration form for STOC participants.

    Validator constraints have to be manually synchronized with:
    - `registration_app/db/migrations` to match the database schema
    """

    anti_harassment_check = BooleanField(
        "Anti Harassment",
        [
            validators.InputRequired(),
        ],
    )

    privacy_policy_postal_mail_opt_out = BooleanField(
        "Postal Mail Opt-Out",
    )
    privacy_policy_email_opt_in = RadioField(
        "E-mail Opt-In",
        [
            validators.InputRequired(),
        ],
        choices=[
            (
                "yes",
                "Yes, please send me ACM Announcements via email",
            ),
            (
                "no",
                "No, please do not send me ACM Announcements via email",
            ),
        ],
    )

    full_name = StringField(
        "Full Name (required)",
        [
            validators.InputRequired(),
            validators.Length(max=512),
        ],
        description="Full name will be printed on the nametag",
    )
    affiliation = StringField(
        "Affiliation",
        description="Your affiliation",
        filters=filter_empty_string_to_none(),
    )

    email = EmailField(
        "Email address (required)",
        [
            validators.InputRequired(),
            validators.Length(max=256),
        ],
        description="This email address will be used to communicate with you",
    )

    acm_membership_number = StringField(
        "ACM Membership number",
        [
            validators.Length(max=64),
        ],
        filters=filter_empty_string_to_none(),
    )
    ieee_membership_number = StringField(
        "IEEE Membership number",
        [
            validators.Length(max=64),
        ],
        filters=filter_empty_string_to_none(),
    )
    is_student = BooleanField(
        "Are you a student?"
    )

    remarks = TextAreaField(
        "Remarks (including dietary restrictions, accessibility requirements, etc.)",
        [
            validators.Length(max=16384),
        ],
        description=(
            "Add any remarks you might have, e.g. dietary restrictions,"
            " accessibility requirements, etc."
        ),
        filters=filter_empty_string_to_none(),
    )

    submit = SubmitField("Register")
