from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database import engine
from app.neo4j_db import check_neo4j

router = APIRouter(tags=["Health"])


@router.get("/health")
def health():
    return {"status": "running"}


@router.get("/health/timescaledb")
def timescaledb_health():
    try:
        with engine.connect() as connection:
            database = connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

            version = connection.execute(
                text("""
                    SELECT extversion
                    FROM pg_extension
                    WHERE extname = 'timescaledb'
                """)
            ).scalar_one_or_none()

        return {
            "status": "connected",
            "database": database,
            "timescaledb_version": version,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="TimescaleDB connection failed",
        ) from exc


@router.get("/health/neo4j")
def neo4j_health():
    try:
        result = check_neo4j()

        return {
            "status": "connected",
            "check": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Neo4j connection failed or is unconfigured",
        ) from exc