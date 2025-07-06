from pydantic import BaseModel, Field
from typing import List

class Competence(BaseModel):
    nom: str
    niveau: int = Field(..., ge=1, le=5, description="Niveau entre 1 et 5")

class FicheEmploye(BaseModel):
    id: int
    nom: str
    prenom: str
    competences: List[Competence]
