from pathlib import Path
from dotenv import load_dotenv

from retrieval.loaders import load_documents
from retrieval.chunking import chunk_documents
from retrieval.vectorstore import build_vectorstore, load_vectorstore

from orchestrator import graph

load_dotenv()


def run_copilot(task):

    if not Path("chroma_db").exists():
        docs = load_documents()
        chunks = chunk_documents(docs)
        vs = build_vectorstore(chunks)
    else:
        vs = load_vectorstore()

    initial_state = {
    "task": task,
    "plan": {},
    "notes": [],
    "draft": "",
    "verification": "",
    "vectorstore": vs,
    "trace": [],
    "metrics": {
        "errors": 0
    }
}



    result = graph.invoke(initial_state)
    return result


if __name__ == "__main__":

    task = "Analyze transportation cost increases and identify possible causes."
    
    result = run_copilot(task)

    print("\n--- FINAL OUTPUT ---\n")
    print(result["draft"])

    print("\n--- VERIFICATION ---\n")
    print(result["verification"])

    print("\n--- TRACE LOG ---\n")
    for step in result["trace"]:
        print(f"{step['agent']} → {step['status']} | {step['details']}")