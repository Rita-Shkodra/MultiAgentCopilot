from langchain_openai import ChatOpenAI


def write_deliverable(task, grounded_notes):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    context = "\n\n".join(
        [f"Citation: {n['citation']}\n{n['summary']}" for n in grounded_notes]
    )

    prompt = f"""
You are an enterprise supply chain analyst.

Use ONLY the grounded notes below.
If something is not supported by the notes, write: "Not found in sources."

TASK:
{task}

GROUNDED NOTES:
{context}

Produce:

1. Executive Summary (max 150 words)
2. Client-ready Email
3. Action List (owner, due date, confidence)
4. Sources (list citation IDs only)
"""

    response = llm.invoke(prompt)

    return response.content
