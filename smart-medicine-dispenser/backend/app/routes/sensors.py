from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.sensor import SensorReadingCreate
from app.services.sensor_service import save_sensor_reading

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/readings", status_code=201)
def create_reading(
    reading: SensorReadingCreate,
    db: Session = Depends(get_db),
):
    try:
        saved = save_sensor_reading(db, reading)
        return {
            "status": "success",
            "reading": saved,
        }

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save sensor reading. Check the dispenser ID and database schema.",
        ) from exc


@router.get("/readings/latest")
def latest_readings(
    limit: int = 10,
    db: Session = Depends(get_db),
):
    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 100",
        )

    from sqlalchemy import text

    query = text("""
        SELECT reading_id, dispenser_id, recorded_at,
               weight_grams, temperature_c, humidity_pct,
               rfid_detected, fingerprint_verified
        FROM public.sensor_readings
        ORDER BY recorded_at DESC
        LIMIT :limit
    """)

    try:
        rows = db.execute(
            query, {"limit": limit}
        ).mappings().all()

        return {"readings": [dict(row) for row in rows]}

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve sensor readings",
        ) from exc