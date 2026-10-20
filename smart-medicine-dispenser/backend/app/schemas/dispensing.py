from datetime import datetime
from pydantic import BaseModel, Field


class DispensingLogCreate(BaseModel):
    dispenser_id: int
    prescription_id: int
    patient_id: int
    medicine_id: int

    dispensed_time: datetime
    dispensed_dosage: str = Field(min_length=1, max_length=50)
    status: str = Field(min_length=1, max_length=30)