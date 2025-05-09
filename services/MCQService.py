from RAGPipeline.instructor_schemas.mcq_schema import MCQsOutput
from RAGPipeline.llm_config import embedder_model, client
from RAGPipeline.prompts import generate_mcq_prompt
from RAGPipeline.vectorstore import QdrantStore


class MCQService:

    def generate_mcqs(self, chat_id: str, query: str):
        # Step 1: Fetch documents
        query_vector = embedder_model.embed_query(query)
        context = QdrantStore.get_context_hits(chat_id,query_vector)
        # Step 2: Build MCQ Prompt
        mcq_prompt = generate_mcq_prompt(context,query)
        # Step 3: Call Gemini Instructor
        response = client.chat.completions.create(
            response_model=MCQsOutput,
            messages=[{"role": "user", "content": mcq_prompt}]
        )

        return response.mcqs