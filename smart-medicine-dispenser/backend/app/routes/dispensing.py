from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.dispensing import DispensingLogCreate
from app.services.dispensing_service import save_dispensing_log

router = APIRouter(prefix="/dispensing", tags=["Dispensing"])


@router.post("/logs", status_code=201)
def create_dispensing_log(
    event: DispensingLogCreate,
    db: Session = Depends(get_db),
):
    # Recording a log is not the same as authorizing a dose.
    # Keep this endpoint for trusted internal testing only.
    try:
        result = save_dispensing_log(db, event)
        return {
            "status": "recorded",
            "event": result,
        }

    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save dispensing log",
        ) from exc