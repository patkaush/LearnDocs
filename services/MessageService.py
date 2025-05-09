
from models import Message
from DbHandler import DbHandler
from sqlalchemy.orm import Session
from datetime import datetime

class MessageService:
    def __init__(self):
        self.handler = DbHandler()

    def add_message(self, chat_id: str, sender: str, content: str):
        db: Session = self.handler.get_db()
        message = Message(chat_id=chat_id, sender=sender, content=content, timestamp=datetime.utcnow())
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_messages(self, chat_id: str):
        db: Session = self.handler.get_db()
        return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp).all()

    def delete_message(self, message_id: int):
        db: Session = self.handler.get_db()
        message = db.query(Message).filter(Message.id == message_id).first()
        if message:
            db.delete(message)
            db.commit()
        return message
