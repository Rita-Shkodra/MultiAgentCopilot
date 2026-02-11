from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        source_path = chunk.metadata.get("source", "unknown")
        filename = Path(source_path).name

        chunk.metadata["citation_id"] = f"{filename}#chunk-{i:03d}"

    print(f"Created {len(chunks)} chunks total.")
    return chunks
