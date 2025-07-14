from typing import List, Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from ..data.training_db import TRAINING_DATABASE
from ..models.recommendation import TrainingRecommendation

class RecommendationEngine:
    def __init__(self):
        self.course_embeddings = self._load_embeddings()
    
    def _load_embeddings(self):
        """Pre-compute all course embeddings"""
        return {
            course["course_id"]: course["embedding"]
            for skill in TRAINING_DATABASE.values()
            for course in skill.values()
        }
    
    def recommend(self, skill_gaps: List[Dict], top_n: int = 3) -> List[TrainingRecommendation]:
        recommendations = []
        for gap in skill_gaps:
            base_courses = self._get_base_courses(gap)
            scored_courses = self._score_courses(base_courses, gap)
            recommendations.extend(scored_courses[:top_n])
        return sorted(recommendations, key=lambda x: x.score, reverse=True)
    
    def _get_base_courses(self, gap: Dict):
        """Find relevant courses from database"""
        skill_name = gap["skill_name"]
        if skill_name in TRAINING_DATABASE:
            return list(TRAINING_DATABASE[skill_name].values())
        return find_similar_courses(skill_name)  # Fallback
        
    def _score_courses(self, courses: List[Dict], gap: Dict) -> List[TrainingRecommendation]:
        """Score courses using multiple factors"""
        scored = []
        for course in courses:
            # 1. Level alignment (30% weight)
            level_score = 1 - abs(gap["required_level"] - course["level"]) * 0.1
            
            # 2. Semantic similarity (40% weight)
            sim_score = cosine_similarity(
                [gap["embedding"]], 
                [course["embedding"]]
            )[0][0]
            
            # 3. Popularity (30% weight)
            pop_score = course.get("popularity", 0.5)
            
            total_score = 0.3*level_score + 0.4*sim_score + 0.3*pop_score
            
            scored.append(TrainingRecommendation(
                course_id=course["course_id"],
                name=course["name"],
                score=total_score,
                match_reason=f"Level {course['level']} {course['skill']} training"
            ))
        return scored