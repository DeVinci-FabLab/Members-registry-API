from sqlalchemy import Column, Integer, Date
from app.db.session import Base

class Member_Training(Base):
    __tablename__ = "member_training"
    
    member_id = Column(Integer, primary_key=True, index=True, foreign_key="member.id")
    training = Column(Integer, primary_key=True, index=True, foreign_key="training.id")
    participation_date = Column(Date, nullable=False)