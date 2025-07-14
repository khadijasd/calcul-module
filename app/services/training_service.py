from typing import List, Dict
from .recommendation_engine import RecommendationEngine
from ..models.recommendation import TrainingRecommendation

engine = RecommendationEngine()

def get_training_recommendations_v2(skill_gaps: List[Dict]) -> List[TrainingRecommendation]:
    """New version with ML recommendations"""
    return engine.recommend(skill_gaps)