from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.db_models import Training, Skill  # tes modèles SQLAlchemy

class TrainingRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_courses(self, skill_name: str, min_level: int, max_level: int) -> List[Dict]:
        trainings = (
            self.db.query(Training)
            .join(Skill)
            .filter(Skill.name == skill_name)
            .filter(Training.level >= min_level, Training.level <= max_level)
            .all()
        )
        return [t.to_dict() for t in trainings]

    def get_all_courses(self) -> List[Dict]:
        trainings = self.db.query(Training).all()
        return [t.to_dict() for t in trainings]
