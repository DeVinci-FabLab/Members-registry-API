from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# === Training ===
class Training(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type_id: int

class TrainingType(BaseModel):
    id: int
    name: str

class MemberTraining(BaseModel):
    member_id: int
    training_id: int
    participation_date: Optional[date]
    status: Optional[str]

# === Trainer ===
class Trainer(BaseModel):
    member_id: int
    training_id: int
    assigned_date: Optional[date]