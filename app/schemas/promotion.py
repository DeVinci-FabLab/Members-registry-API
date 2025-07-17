from pydantic import BaseModel

class Promotion(BaseModel):
    id: int
    year: int
    level: str
    apprentice: bool
    school: int
    major: int

class School(BaseModel):
    id: int
    name: str

class Major(BaseModel):
    id: int
    name: str
    school_id: int