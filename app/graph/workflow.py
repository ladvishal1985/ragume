
from langgraph.graph import StateGraph, START, END
from app.graph.state import State
from app.graph.nodes import retrieve, generate

workflow = StateGraph(State)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app_graph = workflow.compile()
