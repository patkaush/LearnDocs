from pydantic import BaseModel
from typing import List

class QAItem(BaseModel):
    question: str
    answer: str

class QAsOutput(BaseModel):
    qas: List[QAItem]
