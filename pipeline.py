from retrieval.loaders import load_documents
from retrieval.chunking import chunk_documents

if __name__ == "__main__":
    docs = load_documents()
    chunks = chunk_documents(docs)

    print("\nSample chunk:\n")
    print("Citation:", chunks[0].metadata["citation_id"])
    print(chunks[0].page_content[:400])
