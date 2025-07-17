from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    type = Column(Integer, nullable=False, index=True, foreign_key="role_type.id")