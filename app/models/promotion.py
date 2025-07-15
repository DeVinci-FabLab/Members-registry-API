from sqlalchemy import Column, Integer, String, Boolean
from app.db.session import Base

class Contribution(Base):
    __tablename__ = "contribution"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    level = Column(String, nullable=False)
    apprentice = Column(Boolean, nullable=False)
    school_id = Column(Integer, nullable=False, index=True, foreign_key="school.id")
    major_id = Column(Integer, nullable=False, index=True, foreign_key="major.id")
