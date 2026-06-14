from dotenv import load_dotenv

load_dotenv()

from langgraph.graph import StateGraph, START, END

from src.agents.health_agent.state import State
from src.agents.health_agent.nodes.microphone import microphone_node
from src.agents.health_agent.nodes.transcriptor import transcriptor_node
from src.agents.health_agent.nodes.symptom_extractor import symptom_extractor_node

builder = StateGraph(State)
builder.add_node("microphone", microphone_node)
builder.add_node("transcriptor", transcriptor_node)
builder.add_node("symptom_extractor", symptom_extractor_node)

builder.add_edge(START, "microphone")
builder.add_edge("microphone", "transcriptor")
builder.add_edge("transcriptor", "symptom_extractor")
builder.add_edge("symptom_extractor", END)

agent = builder.compile()
