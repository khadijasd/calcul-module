from typing import List, Dict
from ..models.fiche_employe import Employee, SkillLevel
from ..models.fiche_poste import JobDescription, RequiredSkillLevel
from ..models.result import Result, SkillGapDetail



# Calculer le score pour une fiche de poste et un seul employé

def calculate_score_for_employee(job_description: JobDescription, employee: Employee) -> Result:
    skill_gap_details = []
    total_corrected = 0.0
    total_required = 0.0
    bonus_points = 0.0

    # Build a dictionary of employee skills for quick access
    employee_skills: Dict[int, SkillLevel] = {
        skill.skill_id: skill for skill in employee.actual_skills_level
    }

    # Retrieve type weights defined by recruiter
    must_have_weight = job_description.must_have_weight
    nice_to_have_weight = job_description.nice_to_have_weight

    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        skill_name = required_skill.skill_name
        required_level = required_skill.level_value
        skill_weight = required_skill.weight
        skill_type = required_skill.type

        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else 0
        gap = actual_level - required_level
        corrected_level = min(actual_level, required_level)

        # Compute global weight: type weight × individual skill weight
        type_weight = must_have_weight if skill_type == "must_have" else nice_to_have_weight
        global_weight = type_weight * skill_weight

        # Score base contribution
        total_corrected += corrected_level * global_weight
        total_required += required_level * global_weight

        # Bonus if actual level exceeds required
        if actual_level > required_level:
            bonus_points += (actual_level - required_level) * global_weight

        # Store skill gap details
        skill_gap_details.append(SkillGapDetail(
            skill_id=skill_id,
            skill_name=skill_name,
            required_skill_level=required_level,
            actual_skill_level=actual_level,
            gap=gap
        ))

    # Final score calculation (score_base capped at 100)
    score_base = (total_corrected / total_required) * 100 if total_required > 0 else 0
    score_base = round(min(score_base, 100), 2)
    bonus_points = round(bonus_points, 2)

    # Build feedback message
    messages = []
    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        required_level = required_skill.level_value
        skill_name = required_skill.skill_name
        skill_type = required_skill.type

        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else None

        if skill_type == "must_have":
            if actual_level is None:
                messages.append(f"❌ Missing required skill: {skill_name}.")
            elif actual_level < required_level:
                messages.append(
                    f"⚠️ Insufficient level for required skill {skill_name} (required: {required_level}, actual: {actual_level})."
                )
                
        if skill_type == "nice_to_have":
            if actual_level is None or actual_level < required_level:
                messages.append(f"💡 Could improve in nice-to-have skill: {skill_name} (expected: {required_level}, actual: {actual_level}).")


    if not messages:
        messages.append("✅ This employee is a good match for the job.")

    message = "\n".join(messages)
    
    

    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        score_base=score_base,
        bonus=bonus_points,
        skill_gap_details=skill_gap_details,
        message=message
    )
 




# Calculer le score pour une fiche de poste et une liste d'employés

def calculate_score(job_description: JobDescription, employees: List[Employee]) -> List[Result]:
    results = []
    for employee in employees:
        result = calculate_score_for_employee(job_description, employee)
        results.append(result)
    return results



# Filtrer les meilleurs employés


def get_top_employees(results: List[Result], threshold: float = 70.0, top_n: int = 10) -> List[Result]:
    # Filter those with score_base above the threshold
    filtered = [r for r in results if r.score_base >= threshold]

    # Sort descending by score_base only
    sorted_results = sorted(filtered, key=lambda r: r.score_base, reverse=True)

    # Return the top N results
    return sorted_results[:top_n]



