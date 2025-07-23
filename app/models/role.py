from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    type = Column(Integer, ForeignKey("role_type.id"), nullable=False)