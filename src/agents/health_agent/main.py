from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from src.agents.health_agent.state import State
from src.agents.health_agent.nodes.transcriptor import transcriptor_node

builder = StateGraph(State)
builder.add_node("transcriptor", transcriptor_node)

builder.add_edge(START, "transcriptor")
builder.add_edge("transcriptor", END)


agent = builder.compile()
