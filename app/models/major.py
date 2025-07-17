from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Major(Base):
    __tablename__ = "major"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    school_id = Column(Integer, ForeignKey("school.id"), nullable=False, index=True)
