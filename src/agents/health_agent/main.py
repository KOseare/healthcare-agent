from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, START, END
from src.agents.health_agent.state import State

def test_agent(state: State) -> State:
  return {"diagnosis": "You have a cold"}

builder = StateGraph(State)
builder.add_node("transcriptor", test_agent)

builder.add_edge(START, "transcriptor") 
builder.add_edge("transcriptor", END)


agent = builder.compile()