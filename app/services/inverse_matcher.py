from typing import Dict, List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.fiche_employe import Employee
from app.models.fiche_poste import JobDescription
from app.models.result import Result
from app.services.score import calculate_score_for_employee

# Initialisation du modèle SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_jobs_with_cosine_similarity(employee: Employee, job_descriptions: List[JobDescription]) -> List[Dict]:
    """
    Calcule un score de similarité entre les compétences de l'employé et celles requises par les postes,
    en utilisant les embeddings de phrases et la similarité cosinus.
    """

    # Dictionnaire des compétences de l'employé : nom de compétence -> niveau
    employee_skills = {s.skill_name.lower(): s.level_value for s in employee.actual_skills_level}

    def get_vector(text: str) -> np.ndarray:
        """
        Encode un texte en un vecteur dense à l'aide du modèle SentenceTransformer.
        """
        return model.encode(text)

    results = []

    for jd in job_descriptions:
        score = 0
        weight_sum = 0

        for required_skill in jd.required_skills_level:
            req_name = required_skill.skill_name.lower()
            req_vector = get_vector(req_name)

            best_sim = 0
            best_level = 0

            for emp_name, emp_level in employee_skills.items():
                emp_vector = get_vector(emp_name)

                # Calcul de la similarité cosinus entre vecteurs 2D numpy (reshape pour sklearn)
                sim = cosine_similarity(req_vector.reshape(1, -1), emp_vector.reshape(1, -1))[0][0]

                if sim > best_sim:
                    best_sim = sim
                    best_level = emp_level

            # Contribution pondérée au score total selon similarité, niveau et poids
            contrib = best_sim * (min(best_level, required_skill.level_value) / required_skill.level_value) * required_skill.weight
            score += contrib
            weight_sum += required_skill.weight

        # Calcul du score final en pourcentage (s'il y a un poids total)
        final_score = (score / weight_sum) * 100 if weight_sum > 0 else 0

        # Convertir en float natif pour éviter erreur de sérialisation Pydantic (numpy.float32 non supporté)
        final_score = float(final_score)

        results.append({
            "employee_id": employee.employee_id, 
            "job_description_id": jd.job_description_id,
            "similarity_score": round(final_score, 2)
        })

    # Retourner les résultats triés par score décroissant
    return sorted(results, key=lambda x: x["similarity_score"], reverse=True)







def match_jobs_for_employee(employee: Employee, job_descriptions: List[JobDescription]) -> List[Result]:
    results = []
    for jd in job_descriptions:
        result = calculate_score_for_employee(jd, employee)
        results.append(result)
    sorted_results = sorted(results, key=lambda r: r.total_score, reverse=True)
    return sorted_results




