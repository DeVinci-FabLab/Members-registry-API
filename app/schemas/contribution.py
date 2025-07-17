from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class Contribution(BaseModel):
    id: int
    member_id: int
    state: str
    payment_date: Optional[date]
    amount: float
    payment_method: str