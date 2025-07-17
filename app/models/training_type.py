from sqlalchemy import Column, Integer, String, Date
from app.db.base import Base

class Training_Type(Base):
    __tablename__ = "training_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
