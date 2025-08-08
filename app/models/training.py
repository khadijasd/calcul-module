from pydantic import BaseModel
from typing import Optional, List

class TrainingCourse(BaseModel):
    id: int
    name: str
    duration: str
    level: int
    skill_name: str
   # tags: List[str]
    format: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    provider: Optional[str] = None

    class Config:
        orm_mode = True
