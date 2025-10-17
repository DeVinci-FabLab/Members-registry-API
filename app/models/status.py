from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    members = relationship("Member", secondary="member_status", back_populates="statuses")