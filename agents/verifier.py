from langchain_openai import ChatOpenAI


def verify_output(draft, grounded_notes):

    llm = ChatOpenAI(
        model="gpt-4o-mini",   # lightweight but reliable
        temperature=0
    )

    evidence_text = "\n\n".join(
        [f"Citation: {n['citation']}\n{n['fact']}" for n in grounded_notes]
    )

    prompt = f"""
You are a senior audit and compliance verifier.

Your job is to ensure that the draft output is reasonably grounded in the provided evidence.

IMPORTANT:

- The draft may synthesize across multiple sources.
- The draft may logically connect documented risks to cost exposure.
- Executive-level interpretation is allowed.
- Reasonable inference is allowed.

You must ONLY fail the output if:
1. It introduces completely new factors not present in evidence.
2. It invents specific numbers not in evidence.
3. It makes strong causal claims not reasonably implied.
4. It contradicts the evidence.

DO NOT fail for:
- Strategic interpretation
- Logical synthesis
- Business framing
- Risk-based language ("may", "could", "suggests")

Grounded Evidence:
{evidence_text}

Draft Output:
{draft}

Respond in ONE of the following formats:

PASS

OR

FAIL
List clearly unsupported claims.
"""

    response = llm.invoke(prompt)
    return response.content.strip()
