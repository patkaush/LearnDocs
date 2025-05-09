
from pydantic import BaseModel
from datetime import datetime

class MessageInput(BaseModel):
    sender: str
    content: str

class DocumentInput(BaseModel):
    file_name: str
    file_path: str
    content_type: str

from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    file_name: str
    file_path: str
    content_type: str
    uploaded_at: datetime

    class Config:
        from_attributes  = True