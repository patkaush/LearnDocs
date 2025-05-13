import os
import shutil
from datetime import datetime

from sqlalchemy.orm import Session

from DbHandler import DbHandler
from RAGPipeline.loader import DocumentLoader
from models import Document, ChatDocument
from schemas import DocumentResponse


class DocumentService:
    def __init__(self):
        self.handler = DbHandler()
        self.UPLOAD_DIR = "uploads"
    def __copy_file(self,file):
        file_path = os.path.join(self.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path
    def upload_document(self,file,db : Session = None) -> DocumentResponse:
        file_path = self.__copy_file(file)

        document = Document(file_name=file.filename, file_path=file_path, content_type=file.content_type, uploaded_at=datetime.utcnow())

        db.add(document)

        db.flush()

        db.refresh(document)  # <- important
        response = DocumentResponse.from_orm(document)

        return response

    def get_document(self, document_id: int):
        db: Session = self.handler.get_db()
        return db.query(Document).filter(Document.id == document_id).first()
    def upload_parse_document(self,chat_id,file):
        db: Session = self.handler.get_db()
        try:
            document = self.upload_document(file,db)
            link = self.__link_document_to_chat(chat_id, document.id,db)
            loader = DocumentLoader(chat_id,document.file_path)
            loader.load()
            db.commit()
            return document
        except Exception as e:
            db.rollback()  #  rollback everything if failure
            raise Exception( f"Document Parsing failed: {str(e)}")
        finally:
            self.handler.close()

    def __link_document_to_chat(self, chat_id: str, document_id: int,db : Session):
        link = ChatDocument(chat_id=chat_id, document_id=document_id)
        db.add(link)
        db.flush()
        return link

    def get_documents_for_chat(self, chat_id: str):
        db: Session = self.handler.get_db()
        return db.query(Document).join(ChatDocument).filter(ChatDocument.chat_id == chat_id).all()
