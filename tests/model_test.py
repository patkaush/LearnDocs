
from models import Base, Chat, Document, ChatDocument, Message
from DbHandler import init_db, DbHandler
from datetime import datetime

def run_tests():
    init_db()
    db_handler = DbHandler()
    db = db_handler.get_db()

    try:
        # Insert into Chat
        chat = Chat(chat_id="test-chat-id", created_at=datetime.utcnow())
        db.add(chat)
        db.commit()
        db.refresh(chat)
        print("Inserted Chat:", chat)

        # Insert into Document
        document = Document(file_name="example.pdf", file_path="upload/example.pdf", content_type="application/pdf")
        db.add(document)
        db.commit()
        db.refresh(document)
        print("Inserted Document:", document)

        # Insert into ChatDocument
        chat_document = ChatDocument(chat_id="test-chat-id", document_id=document.id)
        db.add(chat_document)
        db.commit()
        db.refresh(chat_document)
        print("Inserted ChatDocument:", chat_document)

        # Insert into Message
        message = Message(chat_id="test-chat-id", sender="user", content="Hello from test!", timestamp=datetime.utcnow())
        db.add(message)
        db.commit()
        db.refresh(message)
        print("Inserted Message:", message)

    finally:
        db_handler.close()

if __name__ == "__main__":
    run_tests()
