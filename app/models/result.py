from pydantic import BaseModel
from typing import List, Dict, Union

from app.models.recommendation import TrainingRecommendation
from app.models.training import TrainingCourse  


class SkillGapDetail(BaseModel):
    skill_id: int
    skill_name: str
    required_skill_level: int
    actual_skill_level: int
    gap: int
    
    
    

class TrainingRecommendation(BaseModel):
    skill_name: str
    gap: int
    recommendations: List[TrainingCourse]

    class Config:
        orm_mode = True
        
        
        
        
        

class Result(BaseModel):
    job_description_id: int
    employee_id: int
    score_base: float         # sur 100 uniquement must_have
    bonus: float              # bonus des nice_to_have
    total_score: float        # somme des deux
    skill_gap_details: List[SkillGapDetail]
    message: str = ""
    feedback: List[str]
    training_recommendations: List[TrainingRecommendation]
 
