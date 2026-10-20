from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/medicines", tags=["Medicines"])


@router.get("/")
def list_medicines(
    db: Session = Depends(get_db),
):
    try:
        rows = db.execute(
            text("""
                SELECT medicine_id, generic_name,
                       chemical_formula, manufacturer,
                       side_effects
                FROM public.medicine
                ORDER BY medicine_id
            """)
        ).mappings().all()

        return {"medicines": [dict(row) for row in rows]}

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve medicines",
        ) from exc