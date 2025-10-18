from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Contribution(Base):
    __tablename__ = "contribution"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.id"), nullable=False, index=True)
    state = Column(String, nullable=False)
    payment_date = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)

    member = relationship("Member", back_populates="contributions")