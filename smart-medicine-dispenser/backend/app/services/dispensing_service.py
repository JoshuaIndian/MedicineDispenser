from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.dispensing import DispensingLogCreate


def save_dispensing_log(
    db: Session,
    event: DispensingLogCreate,
):
    # This function records an event only.
    # It does NOT authorize medication or activate hardware.

    db.execute(
        text("SELECT pg_advisory_xact_lock(731053)")
    )

    log_id = db.execute(
        text("""
            SELECT COALESCE(MAX(log_id), 0) + 1
            FROM public.dispensing_log
        """)
    ).scalar_one()

    values = event.model_dump()
    values["log_id"] = log_id

    query = text("""
        INSERT INTO public.dispensing_log (
            log_id,
            dispenser_id,
            prescription_id,
            patient_id,
            medicine_id,
            dispensed_time,
            dispensed_dosage,
            status
        )
        VALUES (
            :log_id,
            :dispenser_id,
            :prescription_id,
            :patient_id,
            :medicine_id,
            :dispensed_time,
            :dispensed_dosage,
            :status
        )
        RETURNING log_id, dispensed_time, status
    """)

    result = db.execute(
        query,
        values,
    ).mappings().one()

    db.commit()
    return dict(result)