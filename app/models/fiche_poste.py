from pydantic import BaseModel, Field
from typing import List

class CompetenceRequise(BaseModel):
    nom: str
    niveau_min: int = Field(..., ge=1, le=5, description="Niveau minimal requis entre 1 et 5")

class FichePoste(BaseModel):
    poste: str
    competences_requises: List[CompetenceRequise]
