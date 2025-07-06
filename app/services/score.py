def calculer_score(employe_competences: list[str], requises: list[str]) -> float:
    score = len(set(employe_competences) & set(requises)) / len(requises)
    return round(score, 2)

def ecart_competence(employe_competences: list[str], requises: list[str]) -> dict:
    manque = list(set(requises) - set(employe_competences))
    extra = list(set(employe_competences) - set(requises))
    return {"manquantes": manque, "en_trop": extra}

def calculer_top_scores(fiches_employes, fiche_poste, seuil):
    results = []

    for employe in fiches_employes:
        score = calculer_score(employe.competences, fiche_poste.competences_requises)
        if score >= seuil:
            ecart = ecart_competence(employe.competences, fiche_poste.competences_requises)
            results.append({
                "id": employe.id,
                "nom": employe.nom,
                "prenom": employe.prenom,
                "score": score,
                "competences_requises": fiche_poste.competences_requises,
                "competences_acquises": employe.competences,
                "ecart": ecart
            })

    # Trier par score décroissant et renvoyer les 10 premiers
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:10]
