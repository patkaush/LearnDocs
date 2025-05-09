
from fastapi import APIRouter, HTTPException, UploadFile, File, Query

from RAGPipeline.instructor_schemas.mcq_schema import MCQ
from services.ChatService import ChatService
from services.DocumentService import DocumentService
from schemas import MessageInput, DocumentInput, DocumentResponse
from services.FillInBlanksService import FillInBlankService
from services.FlashcardService import FlashcardService
import asyncio

from services.MCQService import MCQService
from services.QAService import QAService

router = APIRouter()
chat_service = ChatService()
document_service = DocumentService()

@router.post("/chat/")
def create_chat():
    return chat_service.create_chat()

@router.get("/chat/{chat_id}")
def get_chat(chat_id: str):
    chat = chat_service.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.get("/chats")
def get_chats():
    chats = chat_service.get_all_chats()
    return chats

@router.post("/chat/{chat_id}/message/")
def send_chat_message(chat_id: str, msg: MessageInput):
    model_response = chat_service.generate_response(chat_id, msg.sender, msg.content)

    return {"content" : model_response}


@router.get("/chat/{chat_id}/messages/")
def get_messages(chat_id: str):
    return chat_service.get_messages(chat_id)

@router.post("/chat/{chat_id}/document")
def upload_document_to_chat(
    chat_id: str,
    file: UploadFile = File(...)
):
    try:
        document = document_service.upload_parse_document(chat_id,file)
        response = DocumentResponse(
            id=document.id,
            file_name=document.file_name,
            file_path=document.file_path,
            content_type=document.content_type,
            uploaded_at=document.uploaded_at,
        )
        return document

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during upload: {str(e)}")


@router.get("/document/{document_id}")
def get_document(document_id: int):
    doc = document_service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/chat/{chat_id}/documents/")
def get_documents_for_chat(chat_id: str):
    return document_service.get_documents_for_chat(chat_id)

@router.delete("/chat/{chat_id}")
def delete_chat(chat_id: str):
    success = chat_service.delete_chat(chat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"detail": "Chat deleted successfully"}
@router.get("/chat/{chat_id}/flashcards")
def get_flashcards(chat_id: str,query: str = Query(..., description="Question to generate flashcards for")):
    try:
        print(query)
        flashcard_service = FlashcardService()
        flashcards = flashcard_service.generate_flashcards(chat_id,query)
        if not flashcards:
            raise HTTPException(status_code=404, detail="No flashcards found or context empty")
        return flashcards
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate flashcards: {str(e)}")
@router.get("/chat/{chat_id}/mcqs")
def get_mcqs(chat_id: str, query: str = Query(..., description="Topic to generate MCQs for")):
    try:
        mcq_service = MCQService()
        mcqs = mcq_service.generate_mcqs(chat_id, query)
        if not mcqs:
            raise HTTPException(status_code=404, detail="No MCQs found or context empty")
        return mcqs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate MCQs: {str(e)}")

@router.get("/chat/{chat_id}/fibs")
def get_fibs(chat_id: str, query: str = Query(..., description="Topic to generate FIBs for")):
    try:
        fib_service = FillInBlankService()
        fibs = fib_service.generate_fibs(chat_id, query)
        if not fibs:
            raise HTTPException(status_code=404, detail="No fill-in-the-blank questions found or context empty")
        return fibs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate fill-in-the-blanks: {str(e)}")

@router.get("/chat/{chat_id}/qas")
def get_qas(chat_id: str, query: str = Query(..., description="Topic to generate Q&A pairs for")):
    try:
        qa_service = QAService()

        qas = qa_service.generate_qas(chat_id, query)
        if not qas:
            raise HTTPException(status_code=404, detail="No Q&A pairs found or context empty")
        return qas
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Q&A pairs: {str(e)}")