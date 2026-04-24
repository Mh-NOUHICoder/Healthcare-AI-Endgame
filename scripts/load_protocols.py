import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.pdf_loader import load_docs_to_chroma

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Look one level up because data directory hasn't been moved yet
    data_dir = os.path.join(os.path.dirname(base_dir), "data")
    
    # Dynamically discover specialties from subdirectories
    specialties = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
    
    for specialty in specialties:
        os.makedirs(os.path.join(data_dir, specialty), exist_ok=True)
        
    print(f"Looking for documents in {data_dir}...")
    load_docs_to_chroma(data_dir)
    print("Ingestion complete.")

if __name__ == "__main__":
    main()
