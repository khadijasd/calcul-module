from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:root@host.docker.internal:5432/training_db"


  # adapte si besoin le port/mot de passe

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency à utiliser dans FastAPI pour injecter la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
