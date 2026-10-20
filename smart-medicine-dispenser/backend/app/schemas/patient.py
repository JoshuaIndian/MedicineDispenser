from pydantic import BaseModel


class PatientLookup(BaseModel):
    person_id: int