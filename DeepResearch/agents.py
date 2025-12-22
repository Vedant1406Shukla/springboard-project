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
def planner_node(state, config):
    llm = get_llm(config)
    search_focus = config.get('configurable', {}).get('search_focus', 'Academic Research Paper')
    
    if search_focus == "Academic Research Paper":
        focus_prompt = "using scientific research papers and academic sources. Focus on retrieving verifiable data from arXiv, ResearchGate, ScienceDirect, etc."
    else:
        focus_prompt = "using general web sources, articles, and news. Provide a broad overview of the topic."

    planner_prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a research planner. Given a user query and conversation history, create a concise step-by-step plan to research the topic {focus_prompt}"),
        ("placeholder", "{chat_history}"),
        ("human", "{query}")
    ])
    
    planner_chain = planner_prompt | llm | StrOutputParser()
    
    query = state['query']
    chat_history = state.get('chat_history', [])
    plan = planner_chain.invoke({"query": query, "chat_history": chat_history})
    return {"plan": plan, "steps": [], "current_step": 0}

# --- Searcher Agent ---
def searcher_node(state, config):
    plan = state['plan']
    query = state['query']
    llm = get_llm(config)
    search_focus = config.get('configurable', {}).get('search_focus', 'Academic Research Paper')
    
    if search_focus == "Academic Research Paper":
        focus_instr = "scientific research papers and academic sources (e.g., adds 'site:arxiv.org OR site:sciencedirect.com' or keywords like 'research paper', 'pdf')"
    else:
        focus_instr = "general web results, blogs, and articles to provide a comprehensive public overview"

    # We can ask the LLM to generate a search query based on the plan
    search_query_prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a search query generator. Based on the research plan and the original query, generate the next best search query to find {focus_instr}. Output ONLY the search query."),
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
def writer_node(state, config):
    llm = get_llm(config)
    query = state['query']
    chat_history = state.get('chat_history', [])
    content = "\n\n".join(state.get('content', []))
    
    # Determine if references should be included
    # Rule: Include if first message OR if it's a completely new topic.
    # We'll use the LLM to decide if it's a "fresh topic" vs "follow-up"
    include_refs = True
    if len(chat_history) > 0:
        decision_prompt = f"Analyze the following query in the context of the conversation. Is this a 'fresh topic' or a 'follow-up' on the previous research? \nQuery: {query}\nAnswer with only 'fresh' or 'follow-up'."
        decision = llm.invoke(decision_prompt).content.strip().lower()
        if "follow-up" in decision:
            include_refs = False

    ref_instruction = ""
    if include_refs:
        ref_instruction = "\n\nIMPORTANT: At the end of your response, you MUST provide a section titled '## References' with a bulleted list of at least 5 URLs/Sources you used from the search results."
    else:
        ref_instruction = "\n\nIMPORTANT: Do NOT include a '## References' section. This is a follow-up inquiry; focus solely on the analysis/methodology asked."

    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a research writer. Synthesize the gathered information to answer the user's query. Incorporate the search results into a cohesive response.{ref_instruction}"),
        ("placeholder", "{chat_history}"),
        ("human", "Query: {query}\n\nSearch Results:\n{content}\n\nProvide a comprehensive answer:")
    ])
    
    writer_chain = writer_prompt | llm | StrOutputParser()
    response = writer_chain.invoke({"query": query, "content": content, "chat_history": chat_history})
    return {"response": response}
