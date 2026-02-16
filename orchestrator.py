from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph
import time

from agents.planner import plan_task
from agents.researcher import research_task
from agents.writer import write_output
from agents.verifier import verify_output


class AgentState(TypedDict):
    task: str
    plan: dict
    notes: List[Dict]
    draft: str
    verification: str
    vectorstore: object
    trace: List[Dict]
    metrics: Dict



def planner_node(state: AgentState):
    t0 = time.time()

    try:
        result = plan_task(state["task"])

        state["plan"] = result.get("content", {})
        tokens = result.get("tokens", {})

        status = "Completed"
        details = f"Generated {len(state['plan'].get('sub_questions', []))} sub-questions"

    except Exception as e:
        status = "ERROR"
        details = str(e)
        state["metrics"]["errors"] += 1
        tokens = {}
        raise

    latency = round((time.time() - t0) * 1000, 2)

    state["trace"].append({
        "agent": "Planner",
        "status": status,
        "details": details,
        "latency_ms": latency,
        "prompt_tokens": tokens.get("prompt_tokens", 0),
        "completion_tokens": tokens.get("completion_tokens", 0),
        "total_tokens": tokens.get("total_tokens", 0)
    })

    return state



def researcher_node(state: AgentState):
    t0 = time.time()

    try:
        vs = state["vectorstore"]
        state["notes"] = research_task(vs, state["plan"])

        status = "Completed"
        details = f"Aggregated {len(state['notes'])} evidence chunks"

    except Exception as e:
        status = "ERROR"
        details = str(e)
        state["metrics"]["errors"] += 1
        raise

    latency = round((time.time() - t0) * 1000, 2)

    state["trace"].append({
        "agent": "Researcher",
        "status": status,
        "details": details,
        "latency_ms": latency,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    })

    return state



def writer_node(state: AgentState):
    t0 = time.time()

    try:
        result = write_output(
            state["task"],
            state["plan"],
            state["notes"]
        )

        state["draft"] = result.get("content", "")
        tokens = result.get("tokens", {})

        status = "Completed"
        details = "Synthesized executive deliverable"

    except Exception as e:
        status = "ERROR"
        details = str(e)
        state["metrics"]["errors"] += 1
        tokens = {}
        raise

    latency = round((time.time() - t0) * 1000, 2)

    state["trace"].append({
        "agent": "Writer",
        "status": status,
        "details": details,
        "latency_ms": latency,
        "prompt_tokens": tokens.get("prompt_tokens", 0),
        "completion_tokens": tokens.get("completion_tokens", 0),
        "total_tokens": tokens.get("total_tokens", 0)
    })

    return state


def verifier_node(state: AgentState):
    t0 = time.time()

    try:
        result = verify_output(
            state["draft"],
            state["notes"]
        )

        state["verification"] = result.get("content", "")
        tokens = result.get("tokens", {})

        status = "PASS" if state["verification"].startswith("PASS") else "FAIL"
        details = "Verification completed"

    except Exception as e:
        status = "ERROR"
        details = str(e)
        state["metrics"]["errors"] += 1
        tokens = {}
        raise

    latency = round((time.time() - t0) * 1000, 2)

    state["trace"].append({
        "agent": "Verifier",
        "status": status,
        "details": details,
        "latency_ms": latency,
        "prompt_tokens": tokens.get("input_tokens", 0),
        "completion_tokens": tokens.get("output_tokens", 0),
        "total_tokens": tokens.get("total_tokens", 0)

    })

    return state



workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("verifier", verifier_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "verifier")
workflow.set_finish_point("verifier")

graph = workflow.compile()
