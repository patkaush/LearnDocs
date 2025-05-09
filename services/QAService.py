from RAGPipeline.llm_config import embedder_model, client
from RAGPipeline.instructor_schemas.qa_schema import QAsOutput
from RAGPipeline.vectorstore import QdrantStore
from RAGPipeline.prompts import generate_qa_prompt

class QAService:

    def generate_qas(self, chat_id: str, query: str):
        # Step 1: Create query vector
        query_vector = embedder_model.embed_query(query)

        # Step 2: Fetch context hits from Qdrant
        context = QdrantStore.get_context_hits(chat_id, query_vector)

        if not context.strip():
            return []

        # Step 3: Build prompt
        qa_prompt = generate_qa_prompt(context, query)

        # Step 4: Call Gemini Instructor
        response = client.chat.completions.create(
            response_model=QAsOutput,
            messages=[{"role": "user", "content": qa_prompt}]
        )

        return response.qas
