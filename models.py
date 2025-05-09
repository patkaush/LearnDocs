
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content_type = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatDocument(Base):
    __tablename__ = 'chat_documents'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, ForeignKey('chats.chat_id'), nullable=False)
    document_id = Column(Integer, ForeignKey('documents.id'), nullable=False)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, ForeignKey('chats.chat_id'), nullable=False)
    sender = Column(String, nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
