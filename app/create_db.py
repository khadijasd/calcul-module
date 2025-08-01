from app.database import Base, engine

# Import all models here so SQLAlchemy knows about them
from app.models.db_models import Skill, Training

Base.metadata.create_all(bind=engine)
