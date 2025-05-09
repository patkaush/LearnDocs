import os
from typing import List
from langchain_unstructured.document_loaders import UnstructuredLoader
from .instructor_schemas.content_schema import Topic
from .llm_config import client
from .prompts import generate_clean_data_prompt
from .vectorstore import QdrantStore

from .text_embedder import TextEmbedder
class DocumentLoader:
    def __init__(self,chat_id ,file_path):
        self.chat_id = chat_id
        self.file_path = file_path


    def load(self):
        raw_data = self.get_raw_data(self.file_path)
        structured_data = self.get_structured_data(raw_data)
        file_name = os.path.basename(self.file_path)

        vectors = TextEmbedder.embed_data(file_name,structured_data)
        store = QdrantStore(collection_name=self.chat_id)
        store.upsert(vectors)
        return None
    def get_raw_data(self,file_path):
        loader = UnstructuredLoader(file_path)  # or .docx, .eml, .html, etc.
        docs = loader.load()
        raw_data = "\n\n".join(doc.page_content for doc in docs)
        return raw_data
    def get_structured_data(self,raw_data):
        try:
            organized_data: List[Topic] = client.chat.completions.create(
                messages=[{"role": "user", "content": generate_clean_data_prompt(raw_data)}],
                response_model=List[Topic],  # Pydantic-driven parsing :contentReference[oaicite:1]{index=1}
                generation_config={
                    "temperature": 0.0,  # fully deterministic
                    # you can also add "max_tokens", "top_p", "top_k", etc.
                }
            )
        except Exception as e:
            print(e)
            raise(e)
        return organized_data
if __name__=="__main__":
    loader = DocumentLoader("attention_test_chat","./attention.pdf")
    loader.load()