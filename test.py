import langchain
import langgraph
import tavily
from importlib.metadata import version

print("✓ LangChain version:", langchain.__version__)
print("✓ LangGraph version:", version("langgraph"))
print("✓ Tavily version:", version("tavily"))
print("\n")