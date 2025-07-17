from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Member_Role(Base):
    __tablename__ = "member_role"
    
    member_id = Column(Integer, ForeignKey("member.id"), primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("role.id"), primary_key=True, index=True)