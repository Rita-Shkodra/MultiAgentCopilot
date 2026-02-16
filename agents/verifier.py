from langchain_openai import ChatOpenAI
from agents.guards import GUARDRAILS


def verify_output(draft, grounded_notes):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    evidence_text = "\n\n".join(
        [f"{n['citation']}\n{n['fact']}" for n in grounded_notes]
    )

    prompt = f"""
{GUARDRAILS}

You are a compliance verifier.

Audit the draft against the evidence.

FAIL only if:
1. A new entity, driver, or event appears.
2. A number is introduced that is not in evidence.
3. A statement contradicts evidence.
4. A mitigation mechanism is invented.

Do NOT fail for:
- Rephrasing
- Logical synthesis
- Executive summarization
- Risk language ("may", "can", "could")

EVIDENCE:
{evidence_text}

DRAFT:
{draft}

Respond EXACTLY:

PASS

OR

FAIL
Unsupported claims:
- <claim>
"""

    response = llm.invoke(prompt)

    usage = getattr(response, "usage_metadata", {}) or {}

    tokens = {
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
    }

    return {
        "content": response.content.strip(),
        "tokens": tokens
    }
