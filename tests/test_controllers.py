
from fastapi.testclient import TestClient
from main import app
import io
import pytest
import os
client = TestClient(app)

@pytest.fixture(scope="module")
def chat_id():
    response = client.post("/chat/")
    assert response.status_code == 200
    data = response.json()
    return data["chat_id"]

def test_send_message(chat_id):
    payload = {
        "sender": "test_user",
        "content": "This is a pytest message."
    }
    response = client.post(f"/chat/{chat_id}/message/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "content" in data

def test_upload_document(chat_id):
    file_content = b"Pytest file content."
    file = io.BytesIO(file_content)
    file.name = "pytest_test.txt"
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    with open(os.path.join(upload_dir, file.name), "wb") as f:
        f.write(file.read())
    response = client.post(
        f"/chat/{chat_id}/document",
        files={"file": ("pytest_test.txt", file, "text/plain")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "file_name" in data

def test_get_messages(chat_id):
    response = client.get(f"/chat/{chat_id}/messages/")
    assert response.status_code == 200
    messages = response.json()
    assert isinstance(messages, list)

def test_get_documents_for_chat(chat_id):
    response = client.get(f"/chat/{chat_id}/documents/")
    assert response.status_code == 200
    documents = response.json()
    assert isinstance(documents, list)

def test_get_all_chats(chat_id):
    response = client.get(f"/chats/")
    assert response.status_code == 200
    chats = response.json()
    print(chats)
    assert isinstance(chats,list)

def test_get_flashcards():
    chat_id = "attention_test_chat"
    response = client.get(f"/chat/{chat_id}/flashcards", params={"query": "Explain transformers"})
    assert response.status_code == 200

    flashcards = response.json()
    assert isinstance(flashcards, list)
    assert len(flashcards) > 0

    # Check structure of a flashcard
    first_card = flashcards[0]
    assert "Q" in first_card
    assert "A" in first_card
    assert isinstance(first_card["Q"], str)
    assert isinstance(first_card["A"], str)

def test_get_mcqs_success():
    chat_id = "attention_test_chat"

    response = client.get(f"/chat/{chat_id}/mcqs", params={"query": "Explain self-attention"})
    assert response.status_code == 200

    mcqs = response.json()
    assert isinstance(mcqs, list)
    assert len(mcqs) > 0

    # Check the structure of a returned MCQ
    first_mcq = mcqs[0]
    assert "question" in first_mcq
    assert "options" in first_mcq
    assert "correct_option" in first_mcq
    assert isinstance(first_mcq["question"], str)
    assert isinstance(first_mcq["options"], list)
    assert len(first_mcq["options"]) == 4  # Exactly 4 options
    assert first_mcq["correct_option"] in ["A", "B", "C", "D"]
def test_get_qas_success():
    test_chat_id = "attention_test_chat"

    response = client.get(f"/chat/{test_chat_id}/qas", params={"query": "Explain transformers"})
    assert response.status_code == 200

    qas = response.json()
    assert isinstance(qas, list)
    assert len(qas) > 0

    # Validate the structure
    first_qa = qas[0]
    assert "question" in first_qa
    assert "answer" in first_qa
    assert isinstance(first_qa["question"], str)
    assert isinstance(first_qa["answer"], str)