"""Database queries regarding a `participant`."""

import logging

from registration_app.model.participant import (
    Participant,
    ParticipantInfo,
)

import psycopg
from bottle import request

logger = logging.getLogger(__name__)


def add_participant(participant: ParticipantInfo) -> int:
    """INSERTs a participant.

    Returns:
        ID of the INSERTed participant.
    """
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO
            participant
            (full_name, affiliation, email, invoicing_address_line_1, invoicing_address_line_2, invoicing_address_city, invoicing_address_country, invoicing_address_zip_code, invoicing_vat_number, participant_type, remarks)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
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
        return cursor.fetchone()[0]  # pyright: ignore


def get_all_participants() -> list[Participant]:
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT full_name, affiliation, email, invoicing_address_line_1,
                   invoicing_address_line_2, invoicing_address_city,
                   invoicing_address_country, invoicing_address_zip_code,
                   invoicing_vat_number, participant_type, remarks, id, date_registered,
                   has_paid
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
                has_paid=r[13],
            )
            for r in results
        ]


def record_successful_payment(id: int) -> ParticipantInfo:
    """Records a successful payment for participant with ID `id`."""
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        cursor.execute(
            """
            UPDATE participant
            SET has_paid = TRUE
            WHERE id = %s
            RETURNING full_name, affiliation, email, invoicing_address_line_1,
                      invoicing_address_line_2, invoicing_address_city,
                      invoicing_address_country, invoicing_address_zip_code,
                      invoicing_vat_number, participant_type, remarks
            """,
            (id,),
        )
        row = cursor.fetchone()
        assert row is not None
        return ParticipantInfo(
            full_name=row[0],
            affiliation=row[1],
            email=row[2],
            invoicing_address_line_1=row[3],
            invoicing_address_line_2=row[4],
            invoicing_address_city=row[5],
            invoicing_address_country=row[6],
            invoicing_address_zip_code=row[7],
            invoicing_vat_number=row[8],
            participant_type=row[9],
            remarks=row[10],
        )


def delete_participant_by_id(id: int) -> None:
    db: psycopg.Connection = request.db
    with db.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM participant
            WHERE id = %s
            """,
            (id,),
        )
