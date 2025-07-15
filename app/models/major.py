from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Major(Base):
    __tablename__ = "major"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    school_id = Column(Integer, nullable=False, index=True, foreign_key="school.id")
    