from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Role_Type(Base):
    __tablename__ = "role_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)