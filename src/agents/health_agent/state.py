from langgraph.graph import MessagesState

class State(MessagesState):
  customer_name: str
  symptoms: list[str]
  personal_data: list[str]
  referred_professional: dict
  diagnosis: str
  transcript: str
  audio_base64: str