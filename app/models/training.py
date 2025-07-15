from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Training(Base):
    __tablename__ = "training"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    type_id = Column(Integer, index=True, foreign_key="training_type.id")