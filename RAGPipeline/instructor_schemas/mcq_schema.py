from pydantic import BaseModel
from typing import List

class MCQOption(BaseModel):
    option: str
    text: str

class MCQ(BaseModel):
    question: str
    options: List[MCQOption]
    correct_option: str

class MCQsOutput(BaseModel):
    mcqs: List[MCQ]
