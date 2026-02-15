from langchain_openai import ChatOpenAI
import json


def write_deliverable(task, grounded_facts):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    context = "\n\n".join(
        [f"Citation: {f['citation']}\n{f['fact']}" for f in grounded_facts]
    )

    prompt = f"""
You are an enterprise supply chain analyst.

STRICT RULES:
- Use ONLY exact text from grounded facts.
- Do NOT paraphrase.
- Do NOT generalize.
- Do NOT introduce new terminology.
- If something is not explicitly present, write: "Not found in sources."

TASK:
{task}

GROUNDED FACTS:
{context}

Return output in STRICT JSON format:

{{
  "executive_summary": [
    {{
      "statement": "...exact text from facts...",
      "citation": "doc#chunk"
    }}
  ],
  "client_email": [
    {{
      "statement": "...exact text from facts...",
      "citation": "doc#chunk"
    }}
  ],
  "action_list": "Not found in sources",
  "sources": ["doc#chunk", "doc#chunk"]
}}
"""

    response = llm.invoke(prompt)

    return response.content
