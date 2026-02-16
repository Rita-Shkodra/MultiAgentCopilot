from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph

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


def planner_node(state: AgentState):
    state["plan"] = plan_task(state["task"])

    state["trace"].append({
        "agent": "Planner",
        "status": "Completed",
        "details": f"Generated {len(state['plan'].get('sub_questions', []))} sub-questions"
    })
    

    return state



def researcher_node(state: AgentState):
    vs = state["vectorstore"]

    state["notes"] = research_task(vs, state["plan"])

    state["trace"].append({
        "agent": "Researcher",
        "status": "Completed",
        "details": f"Aggregated {len(state['notes'])} evidence chunks"
    })
   
    return state



def writer_node(state: AgentState):

    state["draft"] = write_output(
        state["task"],
        state["plan"],
        state["notes"]
    )

    state["trace"].append({
        "agent": "Writer",
        "status": "Completed",
        "details": "Synthesized executive deliverable"
    })

    return state



def verifier_node(state: AgentState):
    state["verification"] = verify_output(state["draft"], state["notes"])
    state["trace"].append({
        "agent": "Verifier",
        "status": "PASS" if state["verification"].startswith("PASS") else "FAIL",
        "details": "Verification completed"
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
