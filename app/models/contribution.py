from sqlalchemy import Column, Integer, String, Date, Float
from app.db.session import Base

class Contribution(Base):
    __tablename__ = "contribution"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, nullable=False, index=True, foreign_key="members.id")
    state : String = Column(String, nullable=False)
    payment_date = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)
    payment_method = Column(String, nullable=False)