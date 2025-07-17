from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class MemberBase(BaseModel):
    last_name: str
    first_name: str
    present: bool
    arrival: Optional[date]
    departure: Optional[date]
    email: Optional[EmailStr]
    personal_email: Optional[EmailStr]
    phone: Optional[str]
    discord: Optional[str]
    notes: Optional[str]
    srg: Optional[bool]
    warning: Optional[int]
    created_by: Optional[str]
    created_at: Optional[date]
    modified_by: Optional[str]
    modified_at: Optional[date]
    convs: Optional[bool]
    portal: Optional[bool]
    promotion_id: Optional[int]

class MemberCreate(MemberBase):
    pass

class MemberRead(MemberBase):
    id: int
    class Config:
        from_attributes = True