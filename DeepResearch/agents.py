import os
import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage

# Remove global LLM init
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Tools
tavily_tool = TavilySearchResults(max_results=5)

# Helper to get LLM
def get_llm(config):
    api_key = config.get('configurable', {}).get('openai_api_key')
    # fallback to env var if not in config
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OpenAI API Key not found. Please set it in the sidebar.")
        
    base_url = None
    if api_key.startswith("sk-or-v1"):
        base_url = "https://openrouter.ai/api/v1"
        
    return ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key, base_url=base_url, max_tokens=1000)

# --- Planner Agent ---
planner_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research planner. Given a user query and conversation history, create a concise step-by-step plan to research the topic using scientific research papers and academic sources. Focus on retrieving verifiable data from arXiv, ResearchGate, ScienceDirect, etc."),
    ("placeholder", "{chat_history}"),
    ("human", "{query}")
])

def planner_node(state, config):
    llm = get_llm(config)
    planner_chain = planner_prompt | llm | StrOutputParser()
    
    query = state['query']
    chat_history = state.get('chat_history', [])
    plan = planner_chain.invoke({"query": query, "chat_history": chat_history})
    return {"plan": plan, "steps": [], "current_step": 0}

# --- Searcher Agent ---
# For simplicity, we will let the LLM decide the search query based on the plan and current context (but the request implies a specific Searcher Agent)

def searcher_node(state, config):
    plan = state['plan']
    query = state['query']
    llm = get_llm(config)
    
    # We can ask the LLM to generate a search query based on the plan
    search_query_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a search query generator. Based on the research plan and the original query, generate the next best search query to find scientific research papers and academic sources (e.g., adds 'site:arxiv.org OR site:sciencedirect.com' or keywords like 'research paper', 'pdf'). Output ONLY the search query."),
        ("human", "Query: {query}\nPlan: {plan}\n\nGenerate search query:")
    ])
    
    chain = search_query_prompt | llm | StrOutputParser()
    
    def generate_query():
        return chain.invoke({"query": query, "plan": plan})
        
    search_query = generate_query()
    
    # Execute search
    try:
        tavily_api_key = config.get('configurable', {}).get('tavily_api_key')
        if not tavily_api_key:
             tavily_api_key = os.environ.get("TAVILY_API_KEY")
        
        limit = random.randint(5, 10)
        tool = TavilySearchResults(max_results=limit, tavily_api_key=tavily_api_key)
        results = tool.invoke(search_query)
        # Check if results is a list (standard output) or string (error)
        if isinstance(results, list):
             content = "\n".join([f"Source: {r.get('url', 'N/A')}\nContent: {r.get('content', 'N/A')}" for r in results])
        else:
             content = str(results)
    except Exception as e:
        content = f"Search failed: {e}"
    
    return {"content": [content]} # Append to content list

# --- Writer Agent ---
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research writer. Synthesize the gathered information to answer the user's query. Incorporate the search results into a cohesive response. \n\nIMPORTANT: At the end of your response, you MUST provide a section titled '## References' with a bulleted list of at least 5 URLs/Sources you used from the search results."),
    ("placeholder", "{chat_history}"),
    ("human", "Query: {query}\n\nSearch Results:\n{content}\n\nProvide a comprehensive answer:")
])

def writer_node(state, config):
    llm = get_llm(config)
    writer_chain = writer_prompt | llm | StrOutputParser()
    
    query = state['query']
    chat_history = state.get('chat_history', [])
    content = "\n\n".join(state.get('content', []))
    response = writer_chain.invoke({"query": query, "content": content, "chat_history": chat_history})
    return {"response": response}
