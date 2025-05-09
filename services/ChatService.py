from qdrant_client.http.exceptions import UnexpectedResponse

from models import Chat, Message, ChatDocument
from DbHandler import DbHandler
from sqlalchemy.orm import Session
from datetime import datetime
import uuid
from RAGPipeline.retriever import *
from RAGPipeline.augmentor import *
from RAGPipeline.generator import *
from RAGPipeline.llm_config import embedder_model,llm
from RAGPipeline.vectorstore import qdrant_client
from langchain.schema import Document
from models import Document as ModelDocument
from langchain.chains.question_answering import load_qa_chain
from RAGPipeline.text_embedder import TextEmbedder
import random
class ChatService:
    def __init__(self):
        self.handler = DbHandler()

    def create_chat(self):
        db: Session = self.handler.get_db()
        chat_id = str(uuid.uuid4())
        chat = Chat(chat_id=chat_id,title = f"User Chat - {random.randint(1,100)}", created_at=datetime.utcnow())
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat

    def get_chat(self, chat_id: str):
        db: Session = self.handler.get_db()
        return db.query(Chat).filter(Chat.chat_id == chat_id).first()
    def get_all_chats(self):
        db = self.handler.get_db()
        try:
            chats = db.query(Chat).all()
            return chats
        finally:
            self.handler.close()
    def add_message(self, chat_id: str, sender: str, content: str):
        db: Session = self.handler.get_db()
        message = Message(chat_id=chat_id, sender=sender, content=content)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_messages(self, chat_id: str):
        db: Session = self.handler.get_db()
        return db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp).all()
    def __get_relevant_context(self,chat_id,query_vector):
        documents = []
        try:

            hits = qdrant_client.query_points(
                collection_name=chat_id,
                query=query_vector,
                limit=5
            )

            for point in hits.points:
                document = Document(
                    page_content=point.payload.get('page_content', ''),
                    metadata={
                        "topic": point.payload.get('topic', ''),
                        "source": point.payload.get('source', '')
                    }
                )
                documents.append(document)
        except UnexpectedResponse as e:
            documents = []
        return documents

    def generate_response(self,chat_id, message_sender, message_content) -> str:
        self.add_message(chat_id, message_sender, message_content)

        # docs = self.retriever.get_vector_store().as_retriever().get_relevant_documents(message_content)
        # message = construct_message([], docs, message_content)
        query_vector = embedder_model.embed_query(message_content)
        documents = self.__get_relevant_context(chat_id,query_vector)

        qa_chain = load_qa_chain(llm, chain_type="stuff")
        answer = qa_chain.run(input_documents=documents, question=message_content)
        self.add_message(chat_id, sender = "bot", content = answer)

        return answer

    def delete_chat(self, chat_id: str) -> bool:
        db = self.handler.get_db()
        try:
            chat = db.query(Chat).filter(Chat.chat_id == chat_id).first()
            if not chat:
                return False

            # First delete all related messages
            db.query(Message).filter(Message.chat_id == chat_id).delete()

            # Then delete all related chat-document links
            linked_documents = (
                db.query(ModelDocument)
                .join(ChatDocument, ChatDocument.document_id == ModelDocument.id)
                .filter(ChatDocument.chat_id == chat_id)
                .all()
            )

            for doc in linked_documents:
                # Remove from Qdrant vectorstore

                qdrant_client.delete_collection(chat_id)

                # Optionally delete document metadata too
                db.delete(doc)
            db.query(ChatDocument).filter(ChatDocument.chat_id == chat_id).delete()

            # Finally delete the chat itself
            db.delete(chat)

            db.commit()
            return True

        except Exception as e:
            db.rollback()
            raise e

        finally:
            self.handler.close()