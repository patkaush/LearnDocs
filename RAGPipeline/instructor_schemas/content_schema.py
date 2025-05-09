from pydantic import BaseModel
from typing import List

class Topic(BaseModel):
    topic: str
    content: str
