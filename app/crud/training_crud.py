from sqlalchemy.orm import Session
from app.models.db_models import Training, Skill
from app.schemas.training_schema import TrainingCreate, TrainingUpdate


# === TRAINING CRUD ===

def create_training(db: Session, training: TrainingCreate):
    db_training = Training(**training.dict())
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training

def get_all_trainings(db: Session):
    return db.query(Training).all()

def get_training_by_id(db: Session, training_id: int):
    return db.query(Training).filter(Training.id == training_id).first()

def update_training(db: Session, training_id: int, training: TrainingUpdate):
    db_training = get_training_by_id(db, training_id)
    if not db_training:
        return None
    for key, value in training.dict().items():
        setattr(db_training, key, value)
    db.commit()
    db.refresh(db_training)
    return db_training

def delete_training(db: Session, training_id: int):
    db_training = get_training_by_id(db, training_id)
    if not db_training:
        return None
    db.delete(db_training)
    db.commit()
    return db_training


