import math
from typing import Dict
from app.models.fiche_employe import Employee, SkillLevel
from app.models.fiche_poste import JobDescription
from app.models.result import Result, SkillGapDetail

def calculate_cosine_similarity_score(job_description: JobDescription, employee: Employee) -> Result:
    employee_skills = {s.skill_id: s for s in employee.actual_skills_level}
    vec_job = []
    vec_emp = []
    skill_gap_details = []

    for skill in job_description.required_skills_level:
        required = skill.level_value
        actual = employee_skills.get(skill.skill_id).level_value if skill.skill_id in employee_skills else 0

        vec_job.append(required)
        vec_emp.append(actual)

        skill_gap_details.append(SkillGapDetail(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            required_skill_level=required,
            actual_skill_level=actual,
            gap=actual - required
        ))

    dot = sum(i * j for i, j in zip(vec_job, vec_emp))
    norm_job = math.sqrt(sum(i ** 2 for i in vec_job))
    norm_emp = math.sqrt(sum(j ** 2 for j in vec_emp))
    similarity = dot / (norm_job * norm_emp) if norm_job * norm_emp != 0 else 0

    final_score = round(similarity * 100, 2)

    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        name=employee.name,
        position=employee.position,
        score_base=final_score,
        bonus=0,
        skill_gap_details=skill_gap_details,
        message="✅ Matched using cosine similarity." if final_score >= 70 else "⚠️ Low vector similarity."
    )
