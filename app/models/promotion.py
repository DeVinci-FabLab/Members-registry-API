from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base

class Promotion(Base):
    __tablename__ = "promotion"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("school.id"), nullable=False)
    major_id = Column(Integer, ForeignKey("major.id"), nullable=True)
    is_apprentice = Column(Boolean, nullable=False)
