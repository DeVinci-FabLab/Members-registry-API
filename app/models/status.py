from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)