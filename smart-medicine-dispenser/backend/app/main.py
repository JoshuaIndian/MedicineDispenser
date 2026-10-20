from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.neo4j_db import close_neo4j
from app.routes import (
    health,
    sensors,
    patients,
    medicines,
    dispensing,
    refills,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_neo4j()


app = FastAPI(
    title="Smart Medicine Dispenser API",
    description=(
        "API for sensor readings, patient data, "
        "medicines, dispensing records, and refills."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(sensors.router)
app.include_router(patients.router)
app.include_router(medicines.router)
app.include_router(dispensing.router)
app.include_router(refills.router)