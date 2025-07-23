from sqlalchemy import Column, Integer, Date, ForeignKey
from app.db.base import Base

class Trainer(Base):
    __tablename__ = "trainer"

    member_id = Column(Integer, ForeignKey("member.id"), primary_key=True)
    training_id = Column(Integer, ForeignKey("training.id") , primary_key=True, nullable=False)
    assigned_date = Column(Date, nullable=False)