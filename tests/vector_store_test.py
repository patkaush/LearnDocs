from qdrant_client import QdrantClient
from RAGPipeline.llm_config import embeddings
client = QdrantClient("http://localhost:6333")

query_text = "Explain how attention works in transformer models."
query_vector = embeddings.embed_query(query_text)

search_results = client.query_points(
    collection_name="final_attention",
    query=query_vector,
    limit=3
)

print(search_results)
