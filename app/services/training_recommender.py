from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from app.models.result import SkillGapDetail
from app.data.training_repository import TrainingRepository
from sentence_transformers import SentenceTransformer
import numpy as np

class TrainingRecommender:
    def __init__(self):
        self.repo = TrainingRepository()
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # Génère des vecteurs automatiquement
        self.skill_vectors: Dict[str, np.ndarray] = {}

    def recommend_detailed(self, gaps: List[SkillGapDetail], employee_skills: Dict[str, int]) -> List[Dict]:
     result = []

     for gap in gaps:
        exact_courses = self.repo.get_courses(
            skill_name=gap.skill_name,
            min_level=gap.actual_skill_level + 1,
            max_level=gap.required_skill_level
        )

        similar_courses = self._find_similar_courses(gap)
        all_courses = exact_courses + similar_courses
        ranked = self._rank_courses(all_courses, gap, employee_skills)

        result.append({
            "skill_name": gap.skill_name,
            "gap": gap.gap,
            "recommendations": ranked[:3]
        })

     return result


    def _find_similar_courses(self, gap: SkillGapDetail) -> List[Dict]:
        target_vector = self._get_vector(gap.skill_name)

        all_courses = self.repo.get_all_courses()  # On récupère toutes les formations disponibles
        similar_courses = []

        for course in all_courses:
            course_skill_name = course["skill_name"]
            if course_skill_name.lower() == gap.skill_name.lower():
                continue  # Ignore la même compétence

            course_vector = self._get_vector(course_skill_name)
            sim = cosine_similarity([target_vector], [course_vector])[0][0]

            if sim > 0.7:
                course["similarity"] = sim
                course["original_gap"] = gap.skill_name
                if course["level"] >= gap.actual_skill_level + 1 and course["level"] <= gap.required_skill_level:
                    similar_courses.append(course)

        return similar_courses

    def _get_vector(self, skill_name: str) -> np.ndarray:
        key = skill_name.lower()
        if key not in self.skill_vectors:
            self.skill_vectors[key] = self.model.encode(key)
        return self.skill_vectors[key]

    def _rank_courses(self, courses: List[Dict], gap: SkillGapDetail, employee_skills: Dict[str, int]) -> List[Dict]:
        def scoring_func(course):
            sim_score = course.get("similarity", 1.0)
            level_diff = course["level"] - gap.actual_skill_level
            level_penalty = 0 if level_diff <= 2 else 0.2 * level_diff

            secondary_bonus = 0
            for tag in course.get("tags", []):
                if tag in employee_skills:
                    secondary_bonus += 0.1 * employee_skills[tag]

            return sim_score - level_penalty + secondary_bonus

        return sorted(courses, key=scoring_func, reverse=True)
    
    
    
    
