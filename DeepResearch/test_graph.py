import os
from dotenv import load_dotenv
from graph import graph
import uuid

load_dotenv()

def test_graph():
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in environment.")
        return
    if not os.environ.get("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY not found in environment.")
        return

    print("Starting Graph Test...")
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    query = "What is the capital of France?"
    print(f"Query: {query}")
    
    inputs = {"query": query, "chat_history": []}
    
    try:
        result = graph.invoke(inputs, config=config)
        print("\n--- Result ---")
        print(result.get("response"))
        print("\n--- Plan ---")
        print(result.get("plan"))
        print("\nTest Complete.")
    except Exception as e:
        print(f"Graph execution failed: {e}")

if __name__ == "__main__":
    test_graph()
