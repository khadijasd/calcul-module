from pydantic import BaseModel
from typing import List

class FichePoste(BaseModel):
    poste: str
    competences_requises: List[str]
