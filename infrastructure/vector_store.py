from typing import List
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from domain.interfaces import IVectorStore
from infrastructure.config import CHROMA_PERSIST_DIR

class VectorStore(IVectorStore):
    def __init__(self):
        self.persist_dir = CHROMA_PERSIST_DIR
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.stores = {}

    def _get_store(self, collection_name: str) -> Chroma:
        if collection_name not in self.stores:
            self.stores[collection_name] = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_dir
            )
        return self.stores[collection_name]

    def similarity_search(self, query: str, collection_name: str, k: int = 3) -> List[dict]:
        store = self._get_store(collection_name)
        docs = store.similarity_search(query, k=k)
        
        results = []
        for doc in docs:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", 0)
            })
        return results
