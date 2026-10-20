from sqlalchemy import text
from sqlalchemy.orm import Session


def get_patient(db: Session, person_id: int):
    query = text("""
        SELECT person_id, address, dob,
               blood_type, emergency_contact
        FROM public.patient
        WHERE person_id = :person_id
    """)

    result = db.execute(
        query,
        {"person_id": person_id},
    ).mappings().first()

    return dict(result) if result else None