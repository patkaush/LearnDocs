from .instructor_schemas.content_schema import Topic
from typing import List
from .llm_config import embedder_model

class TextEmbedder:
    @staticmethod
    def embed_data(source_name : str, source_data : List[Topic]):
        vectors = []
        for idx, data in enumerate(source_data):
            topic_text = data.content
            topic_title = data.topic

            vector = embedder_model.embed_query(topic_text)

            vectors.append({
                "id": idx,
                "vector": vector,
                "payload": {
                    "topic": topic_title,
                    "page_content": topic_text,
                    "source": source_name
                }
            })
        return vectors
