"""Database queries regarding a `participant`."""

import logging
from enum import Enum, auto
from typing import List

from registration_app.model.participant import (
    Participant,
    ParticipantInfo,
    RegistrationFeeType,
)

import psycopg
from bottle import request

logger = logging.getLogger(__name__)


class MembershipType(Enum):
    """Membership types that can apply for a discounted registration fee."""

    ACM = auto()
    IEEE = auto()


def add_participant(
    participant: ParticipantInfo,
    fee_type: RegistrationFeeType,
) -> None:
    """INSERTs a participant."""
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO
            participant
            (postal_mail_opt_out, email_opt_in, full_name, affiliation, email, acm_membership_number, ieee_membership_number, is_student, remarks, fee_type)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                participant.postal_mail_opt_out,
                participant.email_opt_in,
                participant.full_name,
                participant.affiliation,
                participant.email,
                participant.acm_membership_number,
                participant.ieee_membership_number,
                participant.is_student,
                participant.remarks,
                fee_type,
            ),
        )


def get_all_participants() -> List[Participant]:
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT postal_mail_opt_out, email_opt_in, full_name, affiliation, email, acm_membership_number, ieee_membership_number, is_student, remarks, id, date_registered, fee_type
            FROM participant
            ORDER BY date_registered DESC
            """,
        )

        results = cursor.fetchall()
        return [
            Participant(
                postal_mail_opt_out=r[0],
                email_opt_in=r[1],
                full_name=r[2],
                affiliation=r[3],
                email=r[4],
                acm_membership_number=r[5],
                ieee_membership_number=r[6],
                is_student=r[7],
                remarks=r[8],
                id=r[9],
                date_registered=r[10],
                fee_type=r[11],
            )
            for r in results
        ]


def is_membership_unused(
    membership_type: MembershipType,
    membership_number: str,
    provided_email_address: str,
) -> bool:
    """Check if no other participant has the same membership number."""
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        match membership_type:
            case MembershipType.ACM:
                query = """
                SELECT 1
                FROM participant
                WHERE acm_membership_number = %s
                      AND levenshtein(email, %s) < 4
                """
                params = (membership_number, provided_email_address)
            case MembershipType.IEEE:
                query = """
                SELECT 1
                FROM participant
                WHERE ieee_membership_number = %s
                      AND levenshtein(email, %s) < 4
                """
                params = (membership_number, provided_email_address)
        cursor.execute(query, params)
        res = cursor.fetchone()
        return res is None
