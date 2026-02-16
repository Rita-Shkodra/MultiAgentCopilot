from langchain_openai import ChatOpenAI
import json


def plan_task(task: str):

    llm = ChatOpenAI(
        model="gpt-4o-mini",   
        temperature=0
    )

    prompt = f"""
You are a senior supply chain strategy consultant.

Transform the business task below into a structured investigation plan.

Business Task:
{task}

Return ONLY valid JSON with this structure:

{{
  "objective": "...",
  "sub_questions": ["...", "..."],
  "research_queries": ["...", "..."],
  "analysis_focus": ["...", "..."]
}}

Rules:
- Generate 3-5 sub_questions.
- Generate optimized research_queries suitable for document retrieval.
- analysis_focus should reflect key risk or financial dimensions.
- Do not include explanations.
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except Exception:
        
        return {
            "objective": task,
            "sub_questions": [task],
            "research_queries": [task],
            "analysis_focus": []
        }
