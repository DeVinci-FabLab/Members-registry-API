from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.db.base import Base

class Major(Base):
    __tablename__ = "major"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    school_id = Column(Integer, ForeignKey("school.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("level.id"), nullable=False)
    is_alternance = Column(Boolean, default=False, nullable=False)
