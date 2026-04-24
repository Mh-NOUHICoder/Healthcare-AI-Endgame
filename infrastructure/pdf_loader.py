import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from infrastructure.config import CHROMA_PERSIST_DIR

def load_docs_to_chroma(data_dir: str):
    """
    Load PDFs and Text files from specialty folders into Chroma collections.
    """
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist.")
        return

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

    # Discover specialties dynamically
    specialties = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d)) and not d.startswith(".")]

    for specialty in specialties:
        specialty_dir = os.path.join(data_dir, specialty)
        print(f"Processing specialty: {specialty}")
        
        all_splits = []
        for filename in os.listdir(specialty_dir):
            file_path = os.path.join(specialty_dir, filename)
            loader = None
            
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif filename.endswith(".txt") or filename.endswith(".md"):
                loader = TextLoader(file_path, encoding="utf-8")
                
            if loader:
                try:
                    docs = loader.load()
                    # Ensure metadata has 'source' and 'page'
                    for i, doc in enumerate(docs):
                        doc.metadata["source"] = filename
                        doc.metadata["page"] = doc.metadata.get("page", i + 1)
                        
                    splits = text_splitter.split_documents(docs)
                    all_splits.extend(splits)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    continue
                
        if all_splits:
            Chroma.from_documents(
                documents=all_splits,
                embedding=embeddings,
                collection_name=specialty,
                persist_directory=CHROMA_PERSIST_DIR
            )
            print(f"Loaded {len(all_splits)} chunks into {specialty} collection.")
