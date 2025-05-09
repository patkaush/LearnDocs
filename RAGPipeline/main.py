from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA
from langchain_qdrant import QdrantVectorStore
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from RAGPipeline.instructor_schemas.mcq_schema import MCQsOutput
from llm_config import llm, embedder_model,client
from qdrant_client import QdrantClient



query = "What is self-attention?"

query_vector = embedder_model.embed_query(query)

qdrant = QdrantClient(url="http://localhost:6333")
hits = qdrant.query_points(
    collection_name="attention_test_chat",
    query=query_vector,
    limit=5
)

docs = [Document(page_content=point.payload["page_content"]) for point in hits.points]
context = "\n\n".join(d.page_content for d in docs)

mcq_prompt = f"""
You are a helpful Teaching Assistant.

Based on the following context and user query, generate multiple-choice questions (MCQs).

Rules:
- Each MCQ must have 1 correct answer and 3 distractor options.
- Maximum 20 MCQs.
- Return strictly in JSON format:
{{
    "mcqs": [
        {{
            "question": "....",
            "options": [
                {{"option": "A", "text": "..."}},
                {{"option": "B", "text": "..."}},
                {{"option": "C", "text": "..."}},
                {{"option": "D", "text": "..."}}
            ],
            "correct_option": "A"
        }},
        ...
    ]
}}

Context:
{context}

Question:
{query}
"""

# 🔥 Now use your instructor client
mcqs_response = client.chat.completions.create(
    response_model=MCQsOutput,
    messages=[{"role": "user", "content": mcq_prompt}]
)

print("\n🔥 MCQs Generated:")
for idx, mcq in enumerate(mcqs_response.mcqs, 1):
    print(f"\n{idx}. {mcq.question}")
    for opt in mcq.options:
        print(f"{opt.option}: {opt.text}")
    print(f"✅ Correct Answer: {mcq.correct_option}")