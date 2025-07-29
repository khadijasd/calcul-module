from typing import List, Dict
from app.models.fiche_poste import JobDescription
from app.models.fiche_employe import Employee
from app.models.result import Result

from app.services.score import calculate_score_for_employee
from app.services.alternative_score import calculate_alternative_score_for_employee
from app.services.cosine_score import calculate_cosine_similarity_score
from app.services.decay_score import calculate_decay_score_for_employee

def compare_all_formulas(job: JobDescription, employees: List[Employee]) -> List[Dict]:
    comparisons = []

    for e in employees:
        comparison = {
            "employee_id": e.employee_id,
            "name": e.name,
            "position": e.position,
            "results_by_method": {
                "standard": calculate_score_for_employee(job, e),
                "alternative": calculate_alternative_score_for_employee(job, e),
                "cosine": calculate_cosine_similarity_score(job, e),
                "decay": calculate_decay_score_for_employee(job, e),
            }
        }
        comparisons.append(comparison)

    return comparisons
