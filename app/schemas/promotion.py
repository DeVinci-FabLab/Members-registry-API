from typing import Optional
from pydantic import BaseModel


class LevelRead(BaseModel):
    id: int
    name: str
    order: int

    class Config:
        from_attributes = True


class SchoolRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MajorRead(BaseModel):
    id: int
    name: str
    code: str
    school_id: int
    level_id: str
    is_alternance: Optional[bool] = None

    class Config:
        from_attributes = True


class PromotionBase(BaseModel):
    year: int
    level_id: int
    school_id: int
    major_id: Optional[int] = None
    is_apprentice: bool = False


class PromotionCreate(PromotionBase):
    pass


class PromotionRead(PromotionBase):
    id: int
    level: Optional[LevelRead] = None
    school: Optional[SchoolRead] = None
    major: Optional[MajorRead] = None

    class Config:
        from_attributes = True