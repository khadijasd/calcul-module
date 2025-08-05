from typing import List, Dict
from ..models.fiche_employe import Employee, SkillLevel
from ..models.fiche_poste import JobDescription, RequiredSkillLevel
from ..models.result import Result, SkillGapDetail

def calculate_score_for_employee(job_description: JobDescription, employee: Employee) -> Result:
    skill_gap_details = []
    total_corrected = 0.0
    total_required = 0.0
    bonus_points = 0.0

    employee_skills: Dict[int, SkillLevel] = {
        skill.skill_id: skill for skill in employee.actual_skills_level
    }

    must_have_weight = job_description.must_have_weight
    nice_to_have_weight = job_description.nice_to_have_weight

    feedback = []  # ✅ New field for detailed skill-based feedback

    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        skill_name = required_skill.skill_name
        required_level = required_skill.level_value
        skill_weight = required_skill.weight
        skill_type = required_skill.type

        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else 0
        gap = actual_level - required_level
        corrected_level = min(actual_level, required_level)

        type_weight = must_have_weight if skill_type == "must_have" else nice_to_have_weight
        global_weight = type_weight * skill_weight

        total_corrected += corrected_level * global_weight
        total_required += required_level * global_weight

        if actual_level > required_level:
            bonus_points += (actual_level - required_level) * global_weight

        # Collect detailed feedback per skill
        if actual_level == 0:
            feedback.append(f"❌ Missing skill: {skill_name}")
        elif actual_level < required_level:
            feedback.append(f"⚠️ Needs improvement in {skill_name} (required: {required_level}, actual: {actual_level})")
        elif actual_level == required_level:
            feedback.append(f"✅ Meets expectation in {skill_name}")
        else:  # actual_level > required_level
            feedback.append(f"🌟 Very good in {skill_name} (actual: {actual_level}, required: {required_level})")

        skill_gap_details.append(SkillGapDetail(
            skill_id=skill_id,
            skill_name=skill_name,
            required_skill_level=required_level,
            actual_skill_level=actual_level,
            gap=gap
        ))

    score_base = (total_corrected / total_required) * 100 if total_required > 0 else 0
    score_base = round(min(score_base, 100), 2)
    bonus_points = round(bonus_points, 2)

    # Summary message
    messages = []
    for f in feedback:
        if "❌" in f or "⚠️" in f:
            messages.append("⚠️ Some required skills are missing or below expectations.")
            break
    else:
        messages.append("✅ This employee is a good match for the job.")

    message = "\n".join(messages)

    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        name=employee.name,
        position=employee.position,
        score_base=score_base,
        bonus=bonus_points,
        skill_gap_details=skill_gap_details,
        message=message,
        feedback=feedback  # ✅ include the detailed feedback here
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



