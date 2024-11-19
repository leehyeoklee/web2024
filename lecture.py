from pydantic import BaseModel

class Lecture(BaseModel):
    name: str
    code: str
    credits: int
    time: str
    capacity: int
    professor: str
