from pathlib import Path
from dotenv import load_dotenv

from retrieval.loaders import load_documents
from retrieval.chunking import chunk_documents
from retrieval.vectorstore import build_vectorstore, load_vectorstore

from orchestrator import build_graph

load_dotenv()

if __name__ == "__main__":

    if not Path("chroma_db").exists():
        docs = load_documents()
        chunks = chunk_documents(docs)
        vs = build_vectorstore(chunks)
    else:
        vs = load_vectorstore()

    graph = build_graph()

    initial_state = {
        "task": "Analyze transportation cost increases and identify possible causes.",
        "plan": {},
        "notes": [],
        "draft": "",
        "verification": "",
        "vectorstore": vs
    }

    result = graph.invoke(initial_state)

    print("\n--- VERIFICATION ---\n")
    print(result["verification"])

    if result["verification"].startswith("PASS"):
        print("\n--- FINAL OUTPUT ---\n")
        print(result["draft"])
    else:
        print("\nOutput blocked due to verification failure.")
