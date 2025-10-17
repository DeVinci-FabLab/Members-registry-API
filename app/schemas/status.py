from pydantic import BaseModel

# === Status ===
class Status(BaseModel):
    id: int
    name: str

# === Member_Status ===
class MemberStatus(BaseModel):
    member_id: int
    status_id: int

# === Status Create ===
class StatusCreate(BaseModel):
    pass

class StatusRead(StatusCreate):
    id: int
    name: str
    class Config:
        from_attributes = True