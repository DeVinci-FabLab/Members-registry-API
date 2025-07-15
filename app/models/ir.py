from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base

class IR(Base):
    __tablename__ = "ir"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, nullable=False, index=True, foreign_key="members.id")
    state = Column(String, nullable=False)
    version = Column(Integer, nullable=False)
    signature_date = Column(Date, nullable=False)