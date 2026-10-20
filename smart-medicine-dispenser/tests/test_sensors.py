from datetime import datetime, timezone
from decimal import Decimal

from app.schemas.sensor import SensorReadingCreate


def test_sensor_reading_schema():
    reading = SensorReadingCreate(
        dispenser_id=601,
        recorded_at=datetime.now(timezone.utc),
        weight_grams=Decimal("75.20"),
        temperature_c=Decimal("27.40"),
        humidity_pct=Decimal("68.00"),
        rfid_detected=True,
        fingerprint_verified=True,
    )

    assert reading.dispenser_id == 601
    assert reading.weight_grams == Decimal("75.20")
    assert reading.rfid_detected is True