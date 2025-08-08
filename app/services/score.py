from typing import List, Dict
from app.models.fiche_employe import Employee, SkillLevel
from app.models.fiche_poste import JobDescription
from app.models.result import Result, SkillGapDetail
#from app.services.training_recommender import TrainingRecommender
#from app.data.training_repository import TrainingRepository
#from app.database import SessionLocal

def calculate_score_for_employee(job_description: JobDescription, employee: Employee) -> Result:
    skill_gap_details = []
    total_corrected = 0.0
    total_required = 0.0
    bonus_points = 0.0
    feedback: List[str] = []

    # Create dictionary of employee skills for quick access
    employee_skills: Dict[int, SkillLevel] = {
        skill.skill_id: skill for skill in employee.actual_skills_level
    }

    must_have_weight = job_description.must_have_weight
    nice_to_have_weight = job_description.nice_to_have_weight

    # Prepare gap list for training recommendation
    gaps = []

    for required_skill in job_description.required_skills_level:
        skill_id = required_skill.skill_id
        skill_name = required_skill.skill_name
        required_level = required_skill.level_value
        skill_weight = required_skill.weight
        skill_type = required_skill.type

        actual_level = employee_skills.get(skill_id).level_value if skill_id in employee_skills else 0
        gap = actual_level - required_level
        corrected_level = min(actual_level, required_level)

        # Compute global weight
        type_weight = must_have_weight if skill_type == "must_have" else nice_to_have_weight
        global_weight = type_weight * skill_weight

        # Score computation
        total_corrected += corrected_level * global_weight
        total_required += required_level * global_weight

        if actual_level > required_level:
            bonus_points += (actual_level - required_level) * global_weight

        # Feedback
        if actual_level == 0:
            feedback.append(f"❌ Missing skill: {skill_name}")
        elif actual_level < required_level:
            feedback.append(f"⚠️ Needs improvement in {skill_name} (required: {required_level}, actual: {actual_level})")
            gaps.append(SkillGapDetail(
                skill_id=skill_id,
                skill_name=skill_name,
                required_skill_level=required_level,
                actual_skill_level=actual_level,
                gap=required_level - actual_level
            ))
        elif actual_level == required_level:
            feedback.append(f"✅ Meets expectation in {skill_name}")
        else:
            feedback.append(f"🌟 Very good in {skill_name} (actual: {actual_level}, required: {required_level})")

        # Skill gap detail for response
        skill_gap_details.append(SkillGapDetail(
            skill_id=skill_id,
            skill_name=skill_name,
            required_skill_level=required_level,
            actual_skill_level=actual_level,
            gap=gap
        ))

    # 🧠 AI-based training recommendation
   # db = SessionLocal()
    #repo = TrainingRepository(db)
    #recommender = TrainingRecommender(repo)
    #training_recommendations = recommender.recommend_detailed(gaps, {
       # skill.skill_name: skill.level_value for skill in employee.actual_skills_level
    #})
    
    
    
    
    

    # Score calculations
    score_base = (total_corrected / total_required) * 100 if total_required > 0 else 0
    score_base = round(min(score_base, 100), 2)
    bonus_points = round(bonus_points, 2)
    #total_score = round(score_base + bonus_points, 2)

    # Summary message
    if any("❌" in f or "⚠️" in f for f in feedback):
        message = "⚠️ Some required skills are missing or below expectations."
    else:
        message = "✅ This employee is a good match for the job."
        
        
        
        
    

    # ✅ Final result object
    return Result(
        job_description_id=job_description.job_description_id,
        employee_id=employee.employee_id,
        name=employee.name,
        position=employee.position,
        score_base=score_base,
        bonus=bonus_points,
        #total_score=total_score,
        skill_gap_details=skill_gap_details,
        message=message,
        feedback=feedback,
        #training_recommendations=training_recommendations
    )


def calculate_score(job_description: JobDescription, employees: List[Employee]) -> List[Result]:
    results = []
    for employee in employees:
        result = calculate_score_for_employee(job_description, employee)
        results.append(result)
    return results


def get_top_employees(results: List[Result], threshold: float = 70.0, top_n: int = 10) -> List[Result]:
    # Filter those with score_base above the threshold
    filtered = [r for r in results if r.score_base >= threshold]

    # Sort descending by score_base only
    sorted_results = sorted(filtered, key=lambda r: r.score_base, reverse=True)

    # Return the top N results
    return sorted_results[:top_n]
