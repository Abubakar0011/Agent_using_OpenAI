from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


class stateclass(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


model = ChatOpenAI(temperature=0)


def make_graph():
    graph = StateGraph(stateclass)

    def call_mode(state):
        return {"messages": [model.invoke(state["messages"])]}
    
    graph.add_node("agent", call_mode)
    graph.add_edge(START, "agent")
    graph.add_edge("agent", END)

    agent = graph.compile()

    return agent


def make_alternative_graph():
    '''Make a tool calling agent'''

    @tool
    def add(input1: float, input2: float):
        """Adds two numbers."""
        return input1 + input2
    
    tool_node = ToolNode([add])
    model_with_tools = model.bind_tools([add])

    def call_model(state):
        return {"messages": [model_with_tools.invoke(state["messages"])]}
    
    def should_continue(state: stateclass):
        if state["messages"][-1].tool_calls:
            return "tools"
        else:
            return END
        
    graph_workflow = StateGraph(stateclass)
    graph_workflow.add_node("agent", call_model)
    graph_workflow.add_node("tools", tool_node)
    graph_workflow.add_edge("tools", "agent")
    graph_workflow.add_edge(START, "agent")
    graph_workflow.add_conditional_edges("agent", should_continue)

    agent = graph_workflow.compile()
    return agent


agent = make_alternative_graph()


