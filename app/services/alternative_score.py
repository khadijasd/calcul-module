from typing import Dict
from ..models.fiche_employe import Employee, SkillLevel
from ..models.fiche_poste import JobDescription, RequiredSkillLevel
from ..models.result import Result, SkillGapDetail

def calculate_alternative_score_for_employee(job_description: JobDescription, employee: Employee) -> Result:
    skill_gap_details = []
    total_score = 0.0
    total_weight = 0.0
    penalty = 0.0

    # Quick access to employee skill levels
    employee_skills: Dict[int, SkillLevel] = {
        skill.skill_id: skill for skill in employee.actual_skills_level
    }

    must_have_weight = job_description.must_have_weight
    nice_to_have_weight = job_description.nice_to_have_weight

    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        skill_name = required_skill.skill_name
        required_level = required_skill.level_value
        skill_weight = required_skill.weight
        skill_type = required_skill.type

        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else 0
        global_weight = skill_weight * (must_have_weight if skill_type == "must_have" else nice_to_have_weight)

        total_weight += global_weight

        if actual_level >= required_level and required_level > 0:
            # Bonus: non-linear (more reward for exceeding requirement)
            score_contribution = ((actual_level / required_level) ** 1.5) * global_weight
            total_score += score_contribution
        else:
            # Penalty for missing skill, especially must-have
            penalty_factor = 2.0 if skill_type == "must_have" else 1.0
            penalty += (required_level - actual_level) * global_weight * penalty_factor
            score_contribution = (actual_level / required_level) * global_weight if required_level > 0 else 0
            total_score += score_contribution

        skill_gap_details.append(SkillGapDetail(
            skill_id=skill_id,
            skill_name=skill_name,
            required_skill_level=required_level,
            actual_skill_level=actual_level,
            gap=actual_level - required_level
        ))

    raw_score = total_score - penalty
    normalized_score = (raw_score / total_weight) * 100 if total_weight > 0 else 0
    final_score = round(max(0, min(normalized_score, 100)), 2)

    # Build feedback messages
    messages = []
    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        skill_name = required_skill.skill_name
        required_level = required_skill.level_value
        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else 0
        skill_type = required_skill.type

        if skill_type == "must_have":
            if actual_level == 0:
                messages.append(f"❌ Missing required skill: {skill_name}.")
            elif actual_level < required_level:
                messages.append(f"⚠️ Level too low for required skill {skill_name} (required: {required_level}, actual: {actual_level}).")
        elif skill_type == "nice_to_have" and actual_level < required_level:
            messages.append(f"💡 Can improve nice-to-have skill: {skill_name} (expected: {required_level}, actual: {actual_level}).")

    if not messages:
        messages.append("✅ Strong candidate for the position.")

    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        score_base=final_score,
        bonus=0,
        skill_gap_details=skill_gap_details,
        message="\n".join(messages)
    )
