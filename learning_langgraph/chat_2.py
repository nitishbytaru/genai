import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Optional,Literal
from langgraph.graph import StateGraph, START, END
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]

def chatbot(state: State):
    print("Invoking chatbot_1")
    response = client.models.generate_content(
        model = os.getenv("GEMINI_MODEL"),
        contents=state.get("user_query")
    )

    state["llm_output"] = response.text
    return state

def evaluate_response(state: State) -> Literal["chatbot_2","endnode"]:
    if False:
        return "endnode"
    return "chatbot_2"

def chatbot_2(state:State):
    print("Invoking chatbot_2")
    response = client.models.generate_content(
        model = os.getenv("GEMINI_MODEL"),
        contents=state.get("user_query")
    )

    state["llm_output"] = response.text
    return state

def endnode(state:State):
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("chatbot_2",chatbot_2)
graph_builder.add_node("endnode",endnode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_conditional_edges("chatbot",evaluate_response)
graph_builder.add_edge("chatbot_2","endnode")
graph_builder.add_edge("endnode",END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query":"Hi, My name is Nitish Durga"}))
print(updated_state)