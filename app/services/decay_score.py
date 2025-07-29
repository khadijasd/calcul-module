import math
from typing import Dict
from app.models.fiche_employe import Employee, SkillLevel
from app.models.fiche_poste import JobDescription
from app.models.result import Result, SkillGapDetail

def calculate_decay_score_for_employee(job_description: JobDescription, employee: Employee) -> Result:
    employee_skills = {s.skill_id: s for s in employee.actual_skills_level}
    total_weight = 0
    score = 0
    skill_gap_details = []

    for skill in job_description.required_skills_level:
        required = skill.level_value
        actual = employee_skills.get(skill.skill_id).level_value if skill.skill_id in employee_skills else 0

        weight = skill.weight * (
            job_description.must_have_weight if skill.type == "must_have" else job_description.nice_to_have_weight
        )
        ratio = actual / required if required != 0 else 0
        decay_score = math.exp(-abs(1 - ratio)) * weight

        score += decay_score
        total_weight += weight

        skill_gap_details.append(SkillGapDetail(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            required_skill_level=required,
            actual_skill_level=actual,
            gap=actual - required
        ))

    final_score = round((score / total_weight) * 100 if total_weight else 0, 2)

    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        name=employee.name,
        position=employee.position,
        score_base=final_score,
        bonus=0,
        skill_gap_details=skill_gap_details,
        message="✅ Good match using decay." if final_score >= 70 else "⚠️ Weak match."
    )
