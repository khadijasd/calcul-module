from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.skill_schema import SkillCreate, SkillUpdate, SkillOut
from app.crud import skill_crud

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.post("/", response_model=SkillOut)
def create_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    return skill_crud.create_skill(db, skill)

@router.get("/", response_model=list[SkillOut])
def get_all_skills(db: Session = Depends(get_db)):
    return skill_crud.get_skills(db)

@router.get("/{skill_id}", response_model=SkillOut)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = skill_crud.get_skill(db, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return db_skill

@router.put("/{skill_id}", response_model=SkillOut)
def update_skill(skill_id: int, skill: SkillUpdate, db: Session = Depends(get_db)):
    db_skill = skill_crud.update_skill(db, skill_id, skill)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return db_skill

@router.delete("/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    deleted_skill = skill_crud.delete_skill(db, skill_id)
    if not deleted_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"detail": "Skill deleted successfully"}
