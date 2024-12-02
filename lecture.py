from pydantic import BaseModel
from typing import List, Tuple


class Lecture(BaseModel):
    name: str
    code: str
    credits: int
    time: List[Tuple[str, List[int]]]  # ('요일', [시간 리스트]) 형식으로 저장
    classification: str
    capacity: int
    professor: str
