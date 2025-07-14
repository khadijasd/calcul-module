from fastapi import APIRouter
from ...services.recommendation_engine import RecommendationEngine
from ...models.recommendation import RecommendationRequest, TrainingRecommendation

router = APIRouter()
engine = RecommendationEngine()

@router.post("/smart-recommendations", response_model=List[TrainingRecommendation])
async def get_recommendations(request: RecommendationRequest):
    return engine.recommend(request.skill_gaps)