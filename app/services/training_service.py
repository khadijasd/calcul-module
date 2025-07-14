from ..data.training_db import TRAINING_DATABASE
from ..models.fiche_employe import SkillLevel
from ..models.training import TrainingRecommendation  # New model

def get_training_recommendations(
    skill_name: str, 
    current_level: int, 
    target_level: int
) -> List[TrainingRecommendation]:
    recommendations = []
    for level in range(current_level + 1, target_level + 1):
        if skill_name in TRAINING_DATABASE and level in TRAINING_DATABASE[skill_name]:
            recommendations.append(TRAINING_DATABASE[skill_name][level])
    return recommendations