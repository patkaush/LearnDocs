
from models import ChatDocument
from DbHandler import DbHandler
from sqlalchemy.orm import Session

class ChatDocumentService:
    def __init__(self):
        self.handler = DbHandler()

    def link_document_to_chat(self, chat_id: str, document_id: int):
        db: Session = self.handler.get_db()
        link = ChatDocument(chat_id=chat_id, document_id=document_id)
        db.add(link)
        db.commit()
        db.refresh(link)
        return link

    def get_links_for_chat(self, chat_id: str):
        db: Session = self.handler.get_db()
        return db.query(ChatDocument).filter(ChatDocument.chat_id == chat_id).all()

    def delete_link(self, chat_id: str, document_id: int):
        db: Session = self.handler.get_db()
        link = db.query(ChatDocument).filter(ChatDocument.chat_id == chat_id, ChatDocument.document_id == document_id).first()
        if link:
            db.delete(link)
            db.commit()
        return link
