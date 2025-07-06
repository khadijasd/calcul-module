def calculer_score(employe_competences, poste_competences):
    total = len(poste_competences)
    match = 0

    for comp_requise in poste_competences:
        for comp in employe_competences:
            if comp.nom == comp_requise.nom and comp.niveau >= comp_requise.niveau_min:
                match += 1
                break

    return round(match / total, 2) if total > 0 else 0


def ecart_competence(employe_competences, poste_competences):
    manquantes = []
    en_trop = []

    noms_requises = {cr.nom for cr in poste_competences}
    noms_employe = {c.nom for c in employe_competences}

    for cr in poste_competences:
        matching = next((c for c in employe_competences if c.nom == cr.nom), None)
        if not matching or matching.niveau < cr.niveau_min:
            manquantes.append({
                "nom": cr.nom,
                "niveau_requis": cr.niveau_min,
                "niveau_obtenu": matching.niveau if matching else None
            })

    for c in employe_competences:
        if c.nom not in noms_requises:
            en_trop.append({ "nom": c.nom, "niveau": c.niveau })

    return { "manquantes": manquantes, "en_trop": en_trop }


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
