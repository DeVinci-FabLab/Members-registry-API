from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Member_Status(Base):
    __tablename__ = "member_status"

    member_id = Column(Integer, ForeignKey("member.id"), primary_key=True, index=True)
    status_id = Column(Integer, ForeignKey("status.id"), primary_key=True, index=True)