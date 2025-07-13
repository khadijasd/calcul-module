from typing import List, Dict
from ..models.fiche_employe import Employee, SkillLevel
from ..models.fiche_poste import JobDescription, RequiredSkillLevel
from ..models.result import Result, SkillGapDetail



# Calculer le score pour une fiche de poste et un seul employé

def calculate_score_for_employee(job_description: JobDescription, employee: Employee) -> Result:
    skill_gap_details = []
    total_corrected = 0
    total_required = 0
    bonus_points = 0
    missing_must_have_skills = []

    employee_skills: Dict[int, SkillLevel] = {
        skill.skill_id: skill for skill in employee.actual_skills_level
    }

    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        required_level = required_skill.level_value
        weight = required_skill.weight
        skill_type = required_skill.type

        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else 0
        gap = actual_level - required_level
        corrected_level = min(actual_level, required_level)

        if skill_type == "must_have":
            if actual_level < required_level:
                missing_must_have_skills.append(required_skill.skill_name)
            total_corrected += corrected_level * weight
            total_required += required_level * weight

        elif skill_type == "nice_to_have":
            if required_level > 0:
                bonus = (corrected_level / required_level) * weight
                bonus_points += bonus

        skill_gap_details.append(SkillGapDetail(
            skill_id=skill_id,
            skill_name=required_skill.skill_name,
            required_skill_level=required_level,
            actual_skill_level=actual_level,
            gap=gap
        ))

    score_base = (total_corrected / total_required) * 100 if total_required > 0 else 0
    total_score = round(score_base + bonus_points, 2)
    
    messages = []

    for required_skill in job_description.required_skills_level:
       skill_id = required_skill.skill_id
       required_level = required_skill.level_value
       skill_name = required_skill.skill_name
       skill_type = required_skill.type

       actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else None

       if skill_type == "must_have":
         if actual_level is None:
            messages.append(f"❌ Compétence obligatoire manquante : {skill_name}.")
         elif actual_level < required_level:
            messages.append(
                f"⚠️ Niveau insuffisant pour la compétence obligatoire {skill_name} (requis : {required_level}, actuel : {actual_level})."
            )

    if not messages:
        messages.append("✅ Cet employé est un bon fit pour ce poste.")

    message = "\n".join(messages)


    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        score_base=round(score_base, 2),
        bonus=round(bonus_points, 2),
        total_score=total_score,
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
    # Filtrer ceux qui atteignent le seuil
    filtered = [r for r in results if r.score >= threshold]
    # Trier par score décroissant
    sorted_results = sorted(filtered, key=lambda r: r.score, reverse=True)
    # Retourner les top N
    return sorted_results[:top_n]



