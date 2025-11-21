from tavily import TavilyClient
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END

tavily = TavilyClient(api_key="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")


# ---------------------------------------------------------
# UNIVERSAL MESSAGE EXTRACTOR
# ---------------------------------------------------------
def extract_content(msg):
    if hasattr(msg, "content"):
        return msg.content
    if isinstance(msg, dict) and "content" in msg:
        return msg["content"]
    raise ValueError(f"Unknown message format: {msg}")

def get_last_message(state):
    if isinstance(state, dict):
        return state["messages"][-1]
    return state.messages[-1]

def get_last_message_content(state):
    return extract_content(get_last_message(state))
# ---------------------------------------------------------


def tavily_node(state):
    query = get_last_message_content(state)
    results = tavily.search(query)

    return {
        "messages": [
            ToolMessage(
                content=str(results),
                name="tavily_search",
                tool_call_id="tavily_search_1"   # REQUIRED FOR NEW LANGCHAIN
            )
        ]
    }


def mock_llm_node(state):
    tavily_result = get_last_message_content(state)
    return {
        "messages": [
            AIMessage(
                content=f"Here is what Tavily found:\n{tavily_result}"
            )
        ]
    }


graph = StateGraph(MessagesState)
graph.add_node("search", tavily_node)
graph.add_node("llm", mock_llm_node)

graph.add_edge(START, "search")
graph.add_edge("search", "llm")
graph.add_edge("llm", END)

graph = graph.compile()

response = graph.invoke({
    "messages": [
        HumanMessage(content="Who is Leo Messi?")
    ]
})

print(response["messages"][-1].content)
