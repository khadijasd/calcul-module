from typing import List, Dict
from ..models.fiche_employe import Employee, SkillLevel
from ..models.fiche_poste import JobDescription, RequiredSkillLevel
from ..models.result import Result, SkillGapDetail
from ..data.training_db import TRAINING_DATABASE, find_similar_courses
from ..data.skill_embeddings import get_skill_vector

def get_enhanced_training_recommendations(skill_name: str, current_level: int, target_level: int) -> List[Dict]:
    """Enhanced version with fallback to similar skills"""
    recommendations = []
    
    for level in range(current_level + 1, target_level + 1):
        # Try exact match first
        if skill_name in TRAINING_DATABASE and level in TRAINING_DATABASE[skill_name]:
            course = TRAINING_DATABASE[skill_name][level]
            recommendations.append({
                "skill": skill_name,
                "course_id": course["course_id"],
                "course_name": course["name"],
                "level": level,
                "match_type": "exact",
                "duration": course["duration"]
            })
            continue  # Skip similar courses if exact match found
        
        # Fallback to similar skills with proper validation
        similar_courses = find_similar_courses(skill_name)
        for course in similar_courses:
            # Skip if course is missing required fields
            if not isinstance(course, dict) or 'level' not in course:
                continue
            
            try:
                if course["level"] >= level:
                    recommendations.append({
                        "skill": skill_name,
                        "course_id": course.get("course_id", "unknown"),
                        "course_name": f"{course.get('name', 'Unnamed Course')} (covers {skill_name})",
                        "level": course["level"],
                        "match_type": "similar",
                        "duration": course.get("duration", "N/A")
                    })
            except (TypeError, KeyError) as e:
                logging.warning(f"Skipping invalid course: {course}. Error: {str(e)}")
                continue
    
    return recommendations

def calculate_score_for_employee(job_description: JobDescription, employee: Employee) -> Result:
    skill_gap_details = []
    total_corrected = 0
    total_required = 0
    bonus_points = 0
    missing_must_have_skills = []
    training_recommendations = []

    employee_skills: Dict[int, SkillLevel] = {
        skill.skill_id: skill for skill in employee.actual_skills_level
    }

    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        required_level = required_skill.level_value
        weight = required_skill.weight
        skill_type = required_skill.type
        skill_name = required_skill.skill_name

        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else 0
        gap = actual_level - required_level
        corrected_level = min(actual_level, required_level)

        # Generate enhanced training recommendations
        if gap < 0:
            trainings = get_enhanced_training_recommendations(
                skill_name,
                actual_level,
                required_level
            )
            training_recommendations.extend(trainings)

        if skill_type == "must_have":
            if actual_level < required_level:
                missing_must_have_skills.append(skill_name)
            total_corrected += corrected_level * weight
            total_required += required_level * weight
        elif skill_type == "nice_to_have" and required_level > 0:
            bonus_points += (corrected_level / required_level) * weight

        skill_gap_details.append(SkillGapDetail(
            skill_id=skill_id,
            skill_name=skill_name,
            required_skill_level=required_level,
            actual_skill_level=actual_level,
            gap=gap
        ))

    score_base = (total_corrected / total_required) * 100 if total_required > 0 else 0
    total_score = round(score_base + bonus_points, 2)
    
    messages = []
    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else None
        
        if required_skill.type == "must_have":
            if actual_level is None:
                messages.append(f"❌ Missing required skill: {required_skill.skill_name}.")
            elif actual_level < required_skill.level_value:
                messages.append(
                    f"⚠️ Insufficient level for {required_skill.skill_name} "
                    f"(required: {required_skill.level_value}, current: {actual_level})."
                )

    message = "\n".join(messages) if messages else "✅ Good fit for this position."

    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        score_base=round(score_base, 2),
        bonus=round(bonus_points, 2),
        total_score=total_score,
        skill_gap_details=skill_gap_details,
        message=message,
        training_recommendations=sorted(
            training_recommendations,
            key=lambda x: (x["match_type"] == "exact", x["level"]),
            reverse=True
        )[:3]  # Return top 3 recommendations
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



