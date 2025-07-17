from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class InternalRegulation(BaseModel):
    id: int
    member_id: int
    state: str
    version: str
    signature_date: Optional[date]