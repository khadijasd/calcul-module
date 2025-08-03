from typing import List
from pydantic import BaseModel
from app.models.fiche_employe import Employee
from app.models.fiche_poste import JobDescription

class MatchRequest(BaseModel):
    employee: Employee
    job_descriptions: List[JobDescription]
