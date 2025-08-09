from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ensure autoincrement
    name = Column(String(255), unique=True, index=True, nullable=False)  # Unique skill names

    trainings = relationship("Training", back_populates="skill")
    
    
    
    
    
class Training(Base):
    __tablename__ = "trainings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    duration = Column(String(100))
    level = Column(Integer)
    skill_id = Column(Integer, ForeignKey("skills.id"))
    tags = Column(String(255))
    
    # New columns:
    format = Column(String(50))       # 'online' or 'presential'
    location = Column(String(255))    # For presential trainings: place or address
    url = Column(String(500))         # For online trainings: URL link
    provider = Column(String(100))    # e.g. Coursera, Udemy, CodeCamp

    skill = relationship("Skill", back_populates="trainings")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "duration": self.duration,
            "level": self.level,
            "skill_name": self.skill.name if self.skill else None,
            "tags": self.tags.split(",") if self.tags else [],
            "format": self.format,
            "location": self.location,
            "url": self.url,
            "provider": self.provider
        }
