from pydantic import BaseModel
from typing import List, Literal

class RequiredSkillLevel(BaseModel):
    skill_id: int
    skill_name: str
    level_id: int
    level_value: int
    weight: float
    type: Literal["must_have", "nice_to_have"]  # "must_have" ou "nice_to_have"

class JobDescription(BaseModel):
    job_description_id: int
    required_skills_level: List[RequiredSkillLevel]
