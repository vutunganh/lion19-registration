"""Database queries regarding a `participant`."""

import logging

from registration_app.model.participant import (
    Participant,
    ParticipantInfo,
)

import psycopg
from bottle import request

logger = logging.getLogger(__name__)


def add_participant(participant: ParticipantInfo) -> None:
    """INSERTs a participant."""
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO
            participant
            (full_name, affiliation, email, invoicing_address_line_1, invoicing_address_line_2, invoicing_address_city, invoicing_address_country, invoicing_address_zip_code, invoicing_vat_number, participant_type, remarks)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                participant.full_name,
                participant.affiliation,
                participant.email,
                participant.invoicing_address_line_1,
                participant.invoicing_address_line_2,
                participant.invoicing_address_city,
                participant.invoicing_address_country,
                participant.invoicing_address_zip_code,
                participant.invoicing_vat_number,
                participant.participant_type,
                participant.remarks,
            ),
        )


def get_all_participants() -> list[Participant]:
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT full_name, affiliation, email, invoicing_address_line_1,
                   invoicing_address_line_2, invoicing_address_city,
                   invoicing_address_country, invoicing_address_zip_code,
                   invoicing_vat_number, participant_type, remarks, id, date_registered
            FROM participant
            ORDER BY date_registered DESC
            """,
        )

        results = cursor.fetchall()
        return [
            Participant(
                full_name=r[0],
                affiliation=r[1],
                email=r[2],
                invoicing_address_line_1=r[3],
                invoicing_address_line_2=r[4],
                invoicing_address_city=r[5],
                invoicing_address_country=r[6],
                invoicing_address_zip_code=r[7],
                invoicing_vat_number=r[8],
                participant_type=r[9],
                remarks=r[10],
                id=r[11],
                date_registered=r[12],
            )
            for r in results
        ]
