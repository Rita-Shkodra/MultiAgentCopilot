from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict

from agents.planner import plan_task
from agents.researcher import research_task
from agents.writer import write_deliverable
from agents.verifier import verify_output


class AgentState(TypedDict):
    task: str
    plan: dict
    notes: List[Dict]
    draft: str
    verification: str
    vectorstore: object


def planner_node(state: AgentState):
    state["plan"] = plan_task(state["task"])
    return state


def researcher_node(state: AgentState):
    vectorstore = state["vectorstore"]
    state["notes"] = research_task(vectorstore, state["plan"]["search_query"])
    return state


def writer_node(state: AgentState):
    state["draft"] = write_deliverable(state["task"], state["notes"])
    return state


def verifier_node(state: AgentState):
    state["verification"] = verify_output(state["draft"], state["notes"])
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)
    graph.add_node("verifier", verifier_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "verifier")

    graph.set_finish_point("verifier")

    return graph.compile()
