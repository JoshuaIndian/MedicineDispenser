from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class SensorReadingCreate(BaseModel):
    dispenser_id: int

    recorded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    weight_grams: Decimal | None = Field(
        default=None, ge=0
    )
    temperature_c: Decimal | None = None
    humidity_pct: Decimal | None = Field(
        default=None, ge=0, le=100
    )

    rfid_detected: bool = False
    fingerprint_verified: bool = False


class SensorReadingResponse(BaseModel):
    reading_id: int
    dispenser_id: int
    recorded_at: datetime
    weight_grams: Decimal | None
    temperature_c: Decimal | None
    humidity_pct: Decimal | None
    rfid_detected: bool
    fingerprint_verified: bool

    model_config = ConfigDict(from_attributes=True)