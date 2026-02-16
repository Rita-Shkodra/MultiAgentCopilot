from langchain_openai import ChatOpenAI
from agents.guards import GUARDRAILS


def write_output(task, plan, grounded_notes):

    llm = ChatOpenAI(
        model="gpt-4o-mini", 
        temperature=0
    )

    
    evidence_text = "\n\n".join(
        [f"{n['citation']}\n{n['fact']}" for n in grounded_notes]
    )

    prompt = f"""
{GUARDRAILS}

You are an Enterprise Supply Chain Copilot producing a structured executive deliverable.

Your output MUST strictly follow the required structure.

------------------------------------------------------------
TOPIC RELEVANCE RULE
------------------------------------------------------------

If the BUSINESS TASK contains a specific topic, entity, or risk
that does NOT appear anywhere in the EVIDENCE block:

• Explicitly state that no direct evidence was found.
• Do NOT pivot to adjacent risks.
• Do NOT generalize the task.
• Do NOT speculate.

------------------------------------------------------------
EVIDENCE RULES
------------------------------------------------------------

• Only reference entities, drivers, mechanisms, and numbers explicitly present in evidence.
• Do NOT introduce new trends, events, or macro context.
• Do NOT invent strategies.
• Do NOT infer causality unless directly documented.
• Keep wording strength equal to source wording.

------------------------------------------------------------
ACTION DERIVATION RULE
------------------------------------------------------------

You MAY convert documented exposures, pricing mechanisms, cost drivers,
or contractual structures into monitoring or review actions.

If NO documented management lever exists, write EXACTLY:

No documented action identified in retrieved evidence. Missing info needed: <required evidence>

------------------------------------------------------------
STYLE
------------------------------------------------------------

• Executive Summary ≤ 150 words.
• Neutral, analytical tone.
• No exaggeration.
• No repetition.

------------------------------------------------------------
BUSINESS TASK
------------------------------------------------------------

{task}

------------------------------------------------------------
EVIDENCE
------------------------------------------------------------

{evidence_text}

------------------------------------------------------------
REQUIRED OUTPUT STRUCTURE (STRICT)
------------------------------------------------------------

EXECUTIVE SUMMARY:
<text>

CLIENT EMAIL:
Subject: <text>
Greeting: <text>
Body: <text>
Closing: <text>

ACTION LIST:

If actions exist, use EXACTLY this format.
Each field MUST appear on its own line.
Insert ONE blank line between actions.

Action: <text>
Owner: <text>
Due date: <text>
Confidence: <High / Medium / Low>

SOURCES:
<one citation per line>
Format: DocumentName#chunk-id

Do NOT add extra sections.
Do NOT add commentary.
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
