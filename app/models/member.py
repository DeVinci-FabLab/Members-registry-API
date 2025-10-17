from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    present = Column(Boolean, default=False)
    arrival = Column(Date)
    departure = Column(Date)
    email = Column(String, nullable=False, unique=True)
    personal_email = Column(String)
    phone = Column(String)
    discord = Column(String)
    notes = Column(String)
    srg = Column(Boolean, default=False)
    warning = Column(Integer, default=0)
    created_by = Column(String)
    created_at = Column(Date)
    modified_by = Column(String)
    modified_at = Column(Date)
    convs = Column(Boolean, default=False)
    portal = Column(Boolean, default=False)
    promotion_id = Column(Integer, ForeignKey("promotion.id"))

    statuses = relationship("Status", secondary="member_status", back_populates="members")