from langgraph.graph import MessagesState

class State(MessagesState):
  customer_name: str
  symptoms: list[str]
  diagnosis: str