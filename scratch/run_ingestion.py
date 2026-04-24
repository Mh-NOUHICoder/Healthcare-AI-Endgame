import os
import sys

# Add the project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from infrastructure.pdf_loader import load_pdfs_to_chroma

if __name__ == "__main__":
    data_dir = os.path.join(project_root, "data")
    print(f"Loading PDFs from {data_dir}...")
    load_pdfs_to_chroma(data_dir)
    print("Ingestion complete.")
