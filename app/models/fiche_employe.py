from pydantic import BaseModel
from typing import List

class FicheEmploye(BaseModel):
    id: int
    nom: str
    prenom: str
    competences: List[str]
