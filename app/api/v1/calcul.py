from fastapi import APIRouter
from app.models.fiche_employe import FicheEmploye
from app.models.fiche_poste import FichePoste
from app.services.score import calculer_top_scores

router = APIRouter()

@router.post("/scores")
def get_top_scores(fiches_employes: list[FicheEmploye], fiche_poste: FichePoste, seuil: float):
    return calculer_top_scores(fiches_employes, fiche_poste, seuil)
