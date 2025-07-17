from sqlalchemy import Column, Integer, Date
from app.db.session import Base

class Trainer(Base):
    __tablename__ = "trainer"

    member_id = Column(Integer, primary_key=True, index=True, foreign_key="member.id")
    training_id = Column(Integer, primary_key=True ,nullable=False, index=True, foreign_key="training.id")
    assigned_date = Column(Date, nullable=False)