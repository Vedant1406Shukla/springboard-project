from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage
import operator

# Import nodes from agents.py
from agents import planner_node, searcher_node, writer_node

# Define the state with reducers
class AgentState(TypedDict):
    query: str
    plan: str
    content: Annotated[List[str], operator.add]
    response: str
    chat_history: List[BaseMessage]

# Initialize Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("searcher", searcher_node)
workflow.add_node("writer", writer_node)

# Set Entry Point
workflow.set_entry_point("planner")

# Add Edges
workflow.add_edge("planner", "searcher")
workflow.add_edge("searcher", "writer")
workflow.add_edge("writer", END)

# Compile the graph with memory
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
