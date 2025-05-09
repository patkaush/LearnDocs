from pydantic import BaseModel
from typing import List

class Flashcard(BaseModel):
    Q: str
    A: str

class FlashcardsOutput(BaseModel):
    flashcards: List[Flashcard]