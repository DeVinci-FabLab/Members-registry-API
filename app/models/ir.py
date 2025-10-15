from sqlalchemy import Column, Integer, String, Date, ForeignKey
from app.db.base import Base

class IR(Base):
    __tablename__ = "ir"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False, index=True)
    state = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    signature_date = Column(Date, nullable=False)