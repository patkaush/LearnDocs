from RAGPipeline.instructor_schemas.fill_in_blanks_schema import FIBsOutput
from RAGPipeline.llm_config import embedder_model, client
from RAGPipeline.prompts import generate_fib_prompt
from RAGPipeline.vectorstore import QdrantStore


class FillInBlankService:

    def generate_fibs(self, chat_id: str, query: str):
        # Step 1: Fetch documents
        query_vector = embedder_model.embed_query(query)
        context = QdrantStore.get_context_hits(chat_id,query_vector)

        if not context.strip():
            return []

        # Step 2: Prompt for FIB generation
        fib_prompt = generate_fib_prompt(context,query_vector)
        # Step 3: Call Gemini
        response = client.chat.completions.create(
            response_model=FIBsOutput,
            messages=[{"role": "user", "content": fib_prompt}]
        )

        return response.fibs
