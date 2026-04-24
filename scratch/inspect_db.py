import os
import sys
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def inspect_db():
    persist_dir = "./chroma_db"
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    for specialty in ["pediatrics", "cardiology", "drug_safety"]:
        try:
            store = Chroma(
                collection_name=specialty,
                embedding_function=embeddings,
                persist_directory=persist_dir
            )
            count = store._collection.count()
            print(f"Collection '{specialty}' count: {count}")
        except Exception as e:
            print(f"Error checking '{specialty}': {e}")

if __name__ == "__main__":
    inspect_db()
