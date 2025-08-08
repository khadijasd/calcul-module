from typing import Dict, List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.fiche_employe import Employee
from app.models.fiche_poste import JobDescription
from app.models.result import Result
from app.services.score import calculate_score_for_employee







def match_jobs_for_employee(employee: Employee, job_descriptions: List[JobDescription]) -> List[Result]:
    results = []
    for jd in job_descriptions:
        result = calculate_score_for_employee(jd, employee)
        results.append(result)
    sorted_results = sorted(results, key=lambda r: r.score_base, reverse=True)
    return sorted_results




def match_best_jobs_for_all_employees(employees: List[Employee], job_descriptions: List[JobDescription]) -> Dict[int, List[Result]]:
    employee_matches: Dict[int, List[Result]] = {}
    for emp in employees:
        best_jobs = match_jobs_for_employee(emp, job_descriptions)
        employee_matches[emp.employee_id] = best_jobs
    return employee_matches

