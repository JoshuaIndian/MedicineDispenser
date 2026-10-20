from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.patient_service import get_patient

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/{person_id}")
def patient_details(
    person_id: int,
    db: Session = Depends(get_db),
):
    patient = get_patient(db, person_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient