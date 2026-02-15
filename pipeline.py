from pathlib import Path
from dotenv import load_dotenv

from retrieval.loaders import load_documents
from retrieval.chunking import chunk_documents
from retrieval.vectorstore import build_vectorstore, load_vectorstore
from agents.planner import plan_task
from agents.researcher import research_task
from agents.writer import write_deliverable
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

output = write_deliverable(task, notes)

print("\n--- FINAL DELIVERABLE ---\n")
print(output)
