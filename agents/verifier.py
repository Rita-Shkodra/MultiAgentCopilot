import json
import re


def normalize(text):
    return re.sub(r"\s+", " ", text.strip())


def verify_output(draft, grounded_facts):
    try:
        cleaned = draft.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(cleaned)
    except Exception:
        return "FAIL\n- Output is not valid JSON."

    citation_lookup = {
        fact["citation"]: fact["fact"]
        for fact in grounded_facts
    }
    for item in parsed.get("executive_summary", []):
        statement = normalize(item.get("statement", ""))
        citation = item.get("citation", "")

        if citation not in citation_lookup:
            return f"FAIL\n- Citation {citation} not found."

        chunk_text = normalize(citation_lookup[citation])

        if statement not in chunk_text:
            return f"FAIL\n- Statement not supported by cited chunk: {citation}"

   
    for item in parsed.get("client_email", []):
        statement = normalize(item.get("statement", ""))
        citation = item.get("citation", "")

        if citation not in citation_lookup:
            return f"FAIL\n- Citation {citation} not found."

        chunk_text = normalize(citation_lookup[citation])

        if statement not in chunk_text:
            return f"FAIL\n- Statement not supported by cited chunk: {citation}"

    return "PASS"