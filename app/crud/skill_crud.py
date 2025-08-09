from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.db_models import Skill
from app.schemas.skill_schema import SkillCreate, SkillUpdate

def create_skill(db: Session, skill: SkillCreate):
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Skill already exists or ID sequence is broken")
    db.refresh(db_skill)
    return db_skill

def get_skills(db: Session):
    return db.query(Skill).all()

def get_skill(db: Session, skill_id: int):
    return db.query(Skill).filter(Skill.id == skill_id).first()

def update_skill(db: Session, skill_id: int, skill_data: SkillUpdate):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill:
        for key, value in skill_data.dict().items():
            setattr(db_skill, key, value)
        db.commit()
        db.refresh(db_skill)
    return db_skill

def delete_skill(db: Session, skill_id: int):
    db_skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if db_skill:
        db.delete(db_skill)
        db.commit()
    return db_skill
