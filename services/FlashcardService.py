from qdrant_client import QdrantClient
from langchain.schema import Document
from RAGPipeline.retriever import Retriever
from RAGPipeline.instructor_schemas.flashcard_schema import FlashcardsOutput  # Your structured output model
from RAGPipeline.vectorstore import qdrant_client, QdrantStore
from RAGPipeline.llm_config import embedder_model,client
from RAGPipeline.prompts import generate_flashcard_prompt
class FlashcardService:

    def generate_flashcards(self, chat_id: str,query):
        query_vector = embedder_model.embed_query(query)
        context = QdrantStore.get_context_hits(chat_id,query_vector)
        flashcard_message = generate_flashcard_prompt(context,query)
        # Step 3: Call Gemini
        response = client.chat.completions.create(
            response_model=FlashcardsOutput,
            messages=[{"role": "user", "content": flashcard_message}]
        )
        print(response)
        return response.flashcards
