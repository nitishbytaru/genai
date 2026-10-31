import os
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model(
    model=os.getenv("GEMINI_MODEL"),
    model_provider="google_genai",    
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state:State):
    response = llm.invoke(state.get("messages"))
    return {"messages":[response]}

def sample_node(state:State):
    return {"messages":["Sample message appended"]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("sample_node", sample_node)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","sample_node")
graph_builder.add_edge("sample_node",END)


graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages":["Hi, My name is Nitish Durga"]}))
print("updated_state",updated_state)