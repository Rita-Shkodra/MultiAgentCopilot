from langchain_openai import ChatOpenAI
import json
import re
from agents.guards import GUARDRAILS


def safe_parse_json(text: str):
    """
    Never raises JSONDecodeError.
    Always returns a dict.
    """

    if not text or not text.strip():
        return None

    # Remove markdown fences
    cleaned = text.replace("```json", "").replace("```", "").strip()

    # Try direct parse
    try:
        return json.loads(cleaned)
    except:
        pass

    # Try extracting JSON block via regex
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return None


def plan_task(task: str):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
{GUARDRAILS}

You are an enterprise operations and risk analyst.

Break the business task into document-grounded investigation steps.

Return ONLY valid JSON.

Business Task:
{task}

Required JSON format:

{{
  "objective": "...",
  "sub_questions": ["...", "..."],
  "research_queries": ["...", "..."],
  "analysis_focus": ["...", "..."]
}}
"""

    response = llm.invoke(prompt)

    usage = getattr(response, "usage_metadata", {}) or {}

    tokens = {
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0),
    }

    parsed = safe_parse_json(response.content)

    if parsed is None:
        parsed = {
            "objective": task,
            "sub_questions": [],
            "research_queries": [task],
            "analysis_focus": []
        }

    return {
        "content": parsed,
        "tokens": tokens
    }
