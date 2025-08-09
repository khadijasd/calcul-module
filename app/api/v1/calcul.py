from fastapi import APIRouter, Depends
from typing import Dict, List

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.fiche_poste import JobDescription
from app.models.fiche_employe import Employee
from app.models.match_request import MatchRequest
from app.models.result import Result
from app.models.single_calculation_request import SingleCalculationRequest
from app.services.analytics_service import compute_global_statistics
from app.services.inverse_matcher import match_best_jobs_for_all_employees, match_jobs_for_employee
from app.services.score import calculate_score_for_employee
from app.services.score import calculate_score, get_top_employees
from app.services.training_recommender import TrainingRecommender

router = APIRouter()


@router.post("/calculate/one", response_model=Result)
def calculate_one(req: SingleCalculationRequest):
    return calculate_score_for_employee(req.job_description, req.employee)

@router.post("/calculate", response_model=List[Result])
def calculate(job_description: JobDescription, employees: List[Employee]):
    results = calculate_score(job_description, employees)
    return results

@router.post("/calculate/top", response_model=List[Result])
def calculate_top(
    job_description: JobDescription,
    employees: List[Employee],
    threshold: float = 70.0,
    top_n: int = 5 
):
    results = calculate_score(job_description, employees)
    top = get_top_employees(results, threshold=threshold, top_n=top_n)
    return top






@router.post("/evaluate")
async def evaluate_fit(employee: Employee, job: JobDescription):
    recommender = TrainingRecommender()
    recommendations = recommender.recommend(employee, job)
    return {"training_recommendations": recommendations}




@router.post("/statistics/")
def get_statistics(job_description: JobDescription, employees: List[Employee]):
    results = calculate_score(job_description, employees)
    return compute_global_statistics(results)


@router.post("/match-jobs", response_model=List[Result])
def get_matching_jobs_for_employee(request: MatchRequest):
    return match_jobs_for_employee(request.employee, request.job_descriptions)







@router.post("/matching/employees-to-jobs", response_model=Dict[str, List[Result]])
def match_employees_to_jobs(employees: List[Employee], job_descriptions: List[JobDescription]):
    matches = match_best_jobs_for_all_employees(employees, job_descriptions)
    # Convert integer keys to string keys to be JSON compatible
    return {str(employee_id): results for employee_id, results in matches.items()}
