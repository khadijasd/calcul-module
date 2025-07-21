from fastapi import APIRouter, Depends
from app.models.fiche_employe import Employee
from app.models.fiche_poste import JobDescription
from app.models.result import SkillGapDetail
from app.services.training_recommender import TrainingRecommender
from typing import List, Dict

router = APIRouter()

@router.post("/trainings/recommend/clear")
async def recommend_trainings_detailed(
    employee: Employee,
    job: JobDescription,
    recommender: TrainingRecommender = Depends()
):
    employee_skills = {skill.skill_name: skill.level_value for skill in employee.actual_skills_level}
    required_skills = {skill.skill_name: skill.level_value for skill in job.required_skills_level}

    gaps = []
    for skill_name, required_level in required_skills.items():
        actual_level = employee_skills.get(skill_name, 0)
        if required_level > actual_level:
            gap = SkillGapDetail(
                skill_id=0,
                skill_name=skill_name,
                required_skill_level=required_level,
                actual_skill_level=actual_level,
                gap=required_level - actual_level
            )
            gaps.append(gap)

    # Appelle la nouvelle méthode
    detailed_recommendations = recommender.recommend_detailed(gaps, employee_skills)

    return {
        "recommendations_by_gap": detailed_recommendations
    }

