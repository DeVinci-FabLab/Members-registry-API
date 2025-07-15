from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Member_Status(Base):
    __tablename__ = "member_status"

    member_id = Column(Integer, primary_key=True, index=True, foreign_key="member.id")
    status_id = Column(Integer, primary_key=True, index=True, foreign_key="status.id")