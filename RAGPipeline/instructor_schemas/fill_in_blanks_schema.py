from pydantic import BaseModel
from typing import List

class FillInBlank(BaseModel):
    sentence_with_blank: str
    answer: str

class FIBsOutput(BaseModel):
    fibs: List[FillInBlank]
