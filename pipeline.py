from pathlib import Path
from dotenv import load_dotenv

from retrieval.loaders import load_documents
from retrieval.chunking import chunk_documents
from retrieval.vectorstore import build_vectorstore, load_vectorstore
from agents.planner import plan_task
from agents.researcher import research_task

load_dotenv()

if __name__ == "__main__":

    if not Path("chroma_db").exists():
        docs = load_documents()
        chunks = chunk_documents(docs)
        vs = build_vectorstore(chunks)
    else:
        vs = load_vectorstore()

   
    task = "Analyze transportation cost increases and identify possible causes."


    plan = plan_task(task)

    
    notes = research_task(vs, plan["search_query"])

    print("\n--- GROUNDED NOTES ---\n")

    for n in notes:
        print("Citation:", n["citation"])
        print(n["summary"])
        print("-" * 60)
