from pydantic import BaseModel, EmailStr
from typing import Optional 

class Role(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: int

class RoleType(BaseModel):
    id: int
    name: str

class MemberRole(BaseModel):
    member_id: int
    role_id: int
