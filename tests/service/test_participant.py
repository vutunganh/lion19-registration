"""Tests for `registration_app.service.participant` module."""

from registration_app.forms.registration import RegistrationForm
from registration_app.model.participant import ParticipantType
from registration_app.service.participant import determine_participant_type


def test_determine_participant_type() -> None:
    """Tests `determine_participant_type`."""

    test_cases = [
        ("REGULAR", ParticipantType.REGULAR),
        ("STUDENT", ParticipantType.STUDENT),
        ("ACCOMPANYING", ParticipantType.ACCOMPANYING),
    ]

    for input, ref_answer in test_cases:
        form = RegistrationForm()
        form.registration_type.data = input
        assert determine_participant_type(form) == ref_answer
