from sqlalchemy import Column, Integer, String
from app.db.session import Base

class member_role(Base):
    __tablename__ = "member_role"
    
    member_id = Column(Integer, primary_key=True, index=True, foreign_key="member.id")
    role_id = Column(Integer, primary_key=True, index=True, foreign_key="role.id")