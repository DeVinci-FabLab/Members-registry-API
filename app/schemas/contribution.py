from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from schemas import MemberRead


class ContributionBase(BaseModel):
    id: int
    member_id: int
    state: str
    payment_date: Optional[date]
    amount: float

class ContributionCreate(ContributionBase):
    pass

class ContributionRead(ContributionBase):
    id: int
    member: Optional[MemberRead] = None
    state: str
    payment_date: date
    amount: float
    class Config:
        from_attributes = True