from pydantic import BaseModel
from typing import List, Optional

class TrainingRecommendation(BaseModel):
    course_id: str
    name: str
    score: float
    match_reason: str
    metadata: Optional[dict] = None

class RecommendationRequest(BaseModel):
    employee_id: str
    skill_gaps: List[dict]  # [{skill_name, current_level, required_level}]
    preferences: Optional[dict] = None