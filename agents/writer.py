from langchain_openai import ChatOpenAI


def write_output(task, plan, grounded_notes):

    llm = ChatOpenAI(
        model="gpt-4o",   # full model for synthesis
        temperature=0
    )

    # Build evidence context
    evidence_text = "\n\n".join(
        [f"Source: {n['citation']}\n{n['fact']}" for n in grounded_notes]
    )

    prompt = f"""
You are an Enterprise Supply Chain Copilot operating in a risk and compliance context.

Your task is to produce a decision-ready executive deliverable grounded strictly in disclosed evidence.

MANDATORY RULES:

1. Do NOT state that transportation costs are increasing unless explicitly stated in evidence.
2. Do NOT generalize industry-wide conclusions.
3. Do NOT forecast future outcomes.
4. Do NOT invent strategic recommendations.
5. Do NOT infer causality unless clearly documented.
6. Use exposure-based phrasing:
   - "disclosures indicate"
   - "reports document"
   - "evidence highlights"
   - "operations are sensitive to"
   - "results may be affected by"
7. Keep Executive Summary under 150 words.
8. Maintain concise, board-ready, analytical tone.

ACTIONS:
- Only include actions if they are directly tied to documented mechanisms (e.g., fuel surcharge recovery, labor cost exposure).
- If actions cannot be defensibly derived, write:
  "Not found in sources"

Business Task:
{task}

Grounded Evidence:
{evidence_text}

Return output EXACTLY in this structure:

EXECUTIVE SUMMARY:
(max 150 words)

CLIENT EMAIL:
Subject:
Greeting:
Body:
Closing:

ACTION LIST:
- Action:
  Owner:
  Due date:
  Confidence:

SOURCES:
(list unique citations in format DocumentName#chunk-id)

Do not add extra sections.
Do not add commentary.
Do not repeat evidence verbatim.
Synthesize cautiously.
If the draft contains unsupported claims, reduce scope instead of expanding narrative.

"""



    response = llm.invoke(prompt)

    return response.content
