from pydantic import BaseModel
from typing import List

class TrainingRecommendation(BaseModel):
    course_id: str
    name: str
    duration: str
    skill_name: str
    current_level: int
    target_level: int