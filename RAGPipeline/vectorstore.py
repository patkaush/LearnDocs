
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from typing import List,Dict,Any
from langchain.schema import Document

class QdrantStore:
    def __init__(
        self,
        url: str = "http://localhost:6333",
        collection_name: str = "attention_vectors",
        distance: Distance = Distance.COSINE,
    ) -> None:
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.distance = distance
    def ensure_collection(self, vector_size: int) -> None:
        """
        Create the collection in Qdrant if it does not already exist.
        """
        existing = [col.name for col in self.client.get_collections().collections]
        if self.collection_name not in existing:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=self.distance),
            )
    def upsert(self, vectors: List[Dict[str, Any]]) -> None:
        """
        Upsert a list of vector points into the collection.

        Each vector dict must have:
          - 'id': unique identifier (int or str)
          - 'vector': list of floats
          - 'payload': dict of metadata
        """
        if not vectors:
            raise ValueError("No vectors provided for upsert.")

        # Ensure the collection exists with correct dimensions
        first_vector = vectors[0].get("vector")
        if first_vector is None:
            raise KeyError("Each point must include a 'vector' field.")

        vector_size = len(first_vector)
        self.ensure_collection(vector_size)

        # Perform the bulk upsert
        self.client.upsert(
            collection_name=self.collection_name,
            points=vectors,
        )
    def delete_collection(self, collection_name: str):
        try:
            self.client.delete_collection(collection_name=collection_name)
            print(f"Collection '{collection_name}' deleted successfully.")
        except Exception as e:
            print(f"Failed to delete collection {collection_name}: {str(e)}")
    @staticmethod
    def get_context_hits(chat_id,query_vector):
        hits = qdrant_client.query_points(
            collection_name=chat_id,
            query=query_vector,
            limit=5
        )
        docs = [Document(page_content=point.payload["page_content"]) for point in hits.points]

        context = "\n\n".join(d.page_content for d in docs)

        if not context.strip():
            return []
        return context
# store = QdrantStore()
qdrant_client = QdrantClient(url="http://localhost:6333")
