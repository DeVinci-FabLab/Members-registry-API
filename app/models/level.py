from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Level(Base):
    __tablename__ = "level"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    name = Column(String, nullable=False, unique=True)
    order = Column(Integer, nullable=False, unique=True)