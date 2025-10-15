from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from app.db.base import Base

class Contribution(Base):
    __tablename__ = "contribution"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False, index=True)
    state = Column(String, nullable=False)
    payment_date = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)
    payment_method = Column(String, nullable=False)