from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.training_schema import TrainingCreate, TrainingOut, TrainingUpdate
from app.crud import training_crud

router = APIRouter(prefix="/trainings", tags=["Trainings"])


# === Training routes ===

@router.post("/", response_model=TrainingOut)
def create(training: TrainingCreate, db: Session = Depends(get_db)):
    return training_crud.create_training(db, training)

@router.get("/", response_model=List[TrainingOut])
def read_all(db: Session = Depends(get_db)):
    return training_crud.get_all_trainings(db)

@router.get("/{training_id}", response_model=TrainingOut)
def read(training_id: int, db: Session = Depends(get_db)):
    training = training_crud.get_training_by_id(db, training_id)
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")
    return training

@router.put("/{training_id}", response_model=TrainingOut)
def update(training_id: int, training: TrainingUpdate, db: Session = Depends(get_db)):
    updated = training_crud.update_training(db, training_id, training)
    if not updated:
        raise HTTPException(status_code=404, detail="Training not found")
    return updated

@router.delete("/{training_id}")
def delete(training_id: int, db: Session = Depends(get_db)):
    deleted = training_crud.delete_training(db, training_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Training not found")
    return {"message": "Training deleted"}


