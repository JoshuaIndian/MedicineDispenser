from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/refills", tags=["Refills"])


@router.get("/")
def list_refills(
    db: Session = Depends(get_db),
):
    try:
        rows = db.execute(
            text("""
                SELECT *
                FROM public.refill_log
                ORDER BY refill_time DESC
                LIMIT 100
            """)
        ).mappings().all()

        return {"refills": [dict(row) for row in rows]}

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve refill logs",
        ) from exc