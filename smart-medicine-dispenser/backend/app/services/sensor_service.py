from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.sensor import SensorReadingCreate


def save_sensor_reading(
    db: Session,
    reading: SensorReadingCreate,
):
    # Serialize ID generation for requests using this service.
    # The table currently has no default for reading_id.
    db.execute(
        text("SELECT pg_advisory_xact_lock(731052)")
    )

    reading_id = db.execute(
        text("""
            SELECT COALESCE(MAX(reading_id), 0) + 1
            FROM public.sensor_readings
        """)
    ).scalar_one()

    query = text("""
        INSERT INTO public.sensor_readings (
            reading_id,
            dispenser_id,
            recorded_at,
            weight_grams,
            temperature_c,
            humidity_pct,
            rfid_detected,
            fingerprint_verified
        )
        VALUES (
            :reading_id,
            :dispenser_id,
            :recorded_at,
            :weight_grams,
            :temperature_c,
            :humidity_pct,
            :rfid_detected,
            :fingerprint_verified
        )
        RETURNING
            reading_id,
            dispenser_id,
            recorded_at,
            weight_grams,
            temperature_c,
            humidity_pct,
            rfid_detected,
            fingerprint_verified
    """)

    values = reading.model_dump()
    values["reading_id"] = reading_id

    result = db.execute(query, values).mappings().one()
    db.commit()

    return dict(result)