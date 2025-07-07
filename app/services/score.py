from typing import List, Dict
from ..models.fiche_employe import Employee, SkillLevel
from ..models.fiche_poste import JobDescription, RequiredSkillLevel
from ..models.result import Result, SkillGapDetail

def calculate_score(job_description: JobDescription, employees: List[Employee]) -> List[Result]:
    results = []

    for employee in employees:
        skill_gap_details = []
        total_corrected_level = 0  # Somme des niveaux acquis limités au requis
        total_required_level = 0   # Somme des niveaux requis

        # Création d'un dictionnaire des compétences de l'employé pour un accès rapide
        employee_skills: Dict[int, SkillLevel] = {
            skill.skill_id: skill for skill in employee.actual_skills_level
        }

        for required_skill in job_description.required_skills_level:
            required_level = required_skill.level_value
            total_required_level += required_level

            if required_skill.skill_id in employee_skills:
                employee_skill = employee_skills[required_skill.skill_id]
                actual_level = employee_skill.level_value

                # Corriger si le niveau réel dépasse le requis
                corrected_level = min(actual_level, required_level)
                total_corrected_level += corrected_level

                gap = actual_level - required_level

                skill_gap_details.append(SkillGapDetail(
                    skill_id=required_skill.skill_id,
                    skill_name=required_skill.skill_name,
                    required_skill_level=required_level,
                    actual_skill_level=actual_level,
                    gap=gap
                ))
            else:
                # Compétence absente : niveau réel = 0
                gap = -required_level
                total_corrected_level += 0  # Pas de point
                skill_gap_details.append(SkillGapDetail(
                    skill_id=required_skill.skill_id,
                    skill_name=required_skill.skill_name,
                    required_skill_level=required_level,
                    actual_skill_level=0,
                    gap=gap
                ))

        score = (total_corrected_level / total_required_level) * 100 if total_required_level > 0 else 0

        results.append(Result(
            job_description_id=job_description.job_description_id,
            employee_id=employee.employee_id,
            score=round(score, 2),
            skill_gap_details=skill_gap_details
        ))

    return results

#********************************Filtre*********************************



def get_top_employees(results: List[Result], threshold: float = 70.0, top_n: int = 10) -> List[Result]:
    # Filtrer ceux qui atteignent le seuil
    filtered = [r for r in results if r.score >= threshold]
    # Trier par score décroissant
    sorted_results = sorted(filtered, key=lambda r: r.score, reverse=True)
    # Retourner les top N
    return sorted_results[:top_n]