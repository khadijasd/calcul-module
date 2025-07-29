from app.services.alternative_score import calculate_alternative_score_for_employee
from fastapi import APIRouter
from typing import List
from app.models.fiche_poste import JobDescription
from app.models.fiche_employe import Employee
from app.models.result import Result
from app.models.single_calculation_request import SingleCalculationRequest
from app.services.compare_all import compare_all_formulas
from app.services.cosine_score import calculate_cosine_similarity_score
from app.services.decay_score import calculate_decay_score_for_employee
from app.services.score import calculate_score_for_employee
from app.services.score import calculate_score, get_top_employees

router = APIRouter()


@router.post("/calculate/one", response_model=Result)
def calculate_one(req: SingleCalculationRequest):
    return calculate_score_for_employee(req.job_description, req.employee)

@router.post("/calculate", response_model=List[Result])
def calculate(job_description: JobDescription, employees: List[Employee]):
    results = calculate_score(job_description, employees)
    return results

@router.post("/calculate/top", response_model=List[Result])
def calculate_top(job_description: JobDescription, employees: List[Employee], threshold: float = 70.0):
    results = calculate_score(job_description, employees)
    top = get_top_employees(results, threshold=threshold)
    return top



@router.post("/calculate/one/alt", response_model=Result)
def calculate_one_alternative(req: SingleCalculationRequest):
    return calculate_alternative_score_for_employee(req.job_description, req.employee)




# ✅ 3. Cosine Similarity Scoring
@router.post("/calculate/one/cosine", response_model=Result)
def calculate_one_cosine(req: SingleCalculationRequest):
    return calculate_cosine_similarity_score(req.job_description, req.employee)


# ✅ 4. Exponential Decay Scoring
@router.post("/calculate/one/decay", response_model=Result)
def calculate_one_decay(req: SingleCalculationRequest):
    return calculate_decay_score_for_employee(req.job_description, req.employee)


@router.post("/compare")
def compare_all(job_description: JobDescription, employees: List[Employee]):
    return compare_all_formulas(job_description, employees)