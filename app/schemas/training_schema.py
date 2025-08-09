from pydantic import BaseModel
from typing import Optional

class TrainingBase(BaseModel):
    name: str
    duration: str
    level: int
    skill_id: int
    tags: Optional[str] = None
    format: Optional[str] = None
    location: Optional[str] = None
    url: Optional[str] = None
    provider: Optional[str] = None

class TrainingCreate(TrainingBase):
    pass

class TrainingUpdate(TrainingBase):
    pass

class TrainingOut(TrainingBase):
    id: int

    class Config:
        orm_mode = True
