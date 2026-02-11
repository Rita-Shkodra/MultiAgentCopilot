from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

def load_documents(data_path="data/raw"):
    documents = []

    pdf_files = list(Path(data_path).glob("*.pdf"))

    if not pdf_files:
        print("No files found.")
        return []

    for file in pdf_files:
        print(f"Loading {file.name}...")
        loader = PyPDFLoader(str(file))
        docs = loader.load()
        documents.extend(docs)

    print(f"\nLoaded {len(documents)} pages total.")
    return documents
