from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from app.db.session import Base

class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True, index=True)
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
    trainer_id = Column(Integer, ForeignKey("trainer.id"))
    status_id = Column(Integer, ForeignKey("status.id"))
    promotion_id = Column(Integer, ForeignKey("promotion.id"))

