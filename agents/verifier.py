from langchain_openai import ChatOpenAI


def verify_output(draft, grounded_notes):
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    context = "\n\n".join(
        [f"Citation: {n['citation']}\n{n['fact']}" for n in grounded_notes]
    )

    prompt = f"""
You are a STRICT verification agent.

Rules:
- Every factual claim must be directly supported by grounded notes.
- If an action, recommendation, or strategy is NOT explicitly mentioned in the notes, it is unsupported.
- Do NOT assume implied meaning.
- Be extremely strict.

DRAFT OUTPUT:
{draft}

GROUNDED NOTES:
{context}

Respond ONLY in one of these formats:

If ANY unsupported claim exists:
FAIL
- List each unsupported claim clearly.

If EVERYTHING is explicitly supported:
PASS
"""


    response = llm.invoke(prompt)

    return response.content
