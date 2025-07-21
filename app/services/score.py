from typing import List, Dict
from app.models.fiche_employe import Employee, SkillLevel
from app.models.fiche_poste import JobDescription, RequiredSkillLevel
from app.models.result import Result, SkillGapDetail
from app.services.training_recommender import TrainingRecommender

def calculate_score_for_employee(job_description: JobDescription, employee: Employee) -> Result:
    skill_gap_details = []
    total_corrected = 0
    total_required = 0
    bonus_points = 0

    # Dictionnaire pour accès rapide aux niveaux actuels
    employee_skills = {
        skill.skill_name: skill.level_value
        for skill in employee.actual_skills_level
    }

    # 1. Calcul des gaps
    gaps = []
    for required_skill in job_description.required_skills_level:
        skill_name = required_skill.skill_name
        required_level = required_skill.level_value
        actual_level = employee_skills.get(skill_name, 0)
        gap = required_level - actual_level

        if gap > 0:  # Gap positif = compétence à renforcer
            gaps.append(SkillGapDetail(
                skill_id=required_skill.skill_id,
                skill_name=skill_name,
                required_skill_level=required_level,
                actual_skill_level=actual_level,
                gap=gap
            ))

        # Calcul score (must have / nice to have)
        if required_skill.type == "must_have":
            total_corrected += min(actual_level, required_level) * required_skill.weight
            total_required += required_level * required_skill.weight
        elif required_skill.type == "nice_to_have" and required_level > 0:
            bonus_points += min(actual_level, required_level) / required_level * required_skill.weight

        # Ajouter au détail complet
        skill_gap_details.append(SkillGapDetail(
            skill_id=required_skill.skill_id,
            skill_name=skill_name,
            required_skill_level=required_level,
            actual_skill_level=actual_level,
            gap=actual_level - required_level
        ))

    # 2. Recommandations IA
    recommender = TrainingRecommender()
    training_recommendations = recommender.recommend(gaps, employee_skills)

    # 3. Messages d'avertissement
    messages = []
    for required_skill in job_description.required_skills_level:
        if required_skill.type == "must_have":
            actual_level = employee_skills.get(required_skill.skill_name, 0)
            if actual_level < required_skill.level_value:
                messages.append(
                    f"⚠️ Insufficient {required_skill.skill_name} "
                    f"(required: {required_skill.level_value}, current: {actual_level})"
                )

    message = "\n".join(messages) if messages else "✅ Good fit for this position."

    # Calcul score final
    score_base = (total_corrected / total_required) * 100 if total_required > 0 else 0
    total_score = round(score_base + bonus_points, 2)

    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        score_base=round(score_base, 2),
        bonus=round(bonus_points, 2),
        total_score=total_score,
        skill_gap_details=skill_gap_details,
        message=message,
        training_recommendations=training_recommendations
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



