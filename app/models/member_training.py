from sqlalchemy import Column, Integer, Date, ForeignKey
from app.db.base import Base

class Member_Training(Base):
    __tablename__ = "member_training"
    
    member_id = Column(Integer, ForeignKey("member.id"), primary_key=True)
    training = Column(Integer, ForeignKey("training.id"), primary_key=True)
    participation_date = Column(Date, nullable=False)