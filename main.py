# ============================================================
# MODULAR RESEARCH AGENT WORKFLOW (GEMINI + TAVILY)
# ============================================================

# ------------------------ IMPORTS ---------------------------
from langgraph.graph import StateGraph, END
from tavily import TavilyClient
import google.generativeai as genai
import json
import os


# ============================================================
# API KEY LOADING
# ============================================================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY NOT FOUND in environment variables")

if not TAVILY_API_KEY:
    raise ValueError("❌ TAVILY_API_KEY NOT FOUND in environment variables")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# Tavily
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


# ============================================================
# INITIAL STATE STRUCTURE
# ============================================================

def create_initial_state(user_query: str):
    return {
        "user_query": user_query,
        "plan": "",
        "search_results": {},
        "final_answer": ""
    }


# ============================================================
# AGENT 1 — PLANNER (Gemini)
# ============================================================

def planner_agent(state):
    print("\n================ PLANNER AGENT START ================")

    query = state["user_query"]

    prompt = f"""
You are a planning agent. Break down the topic into clear,
actionable research steps.

Topic: {query}

Return a structured plan.
"""

    response = gemini_model.generate_content(prompt)
    plan_text = response.text.strip()

    print("\n📌 PLAN GENERATED:\n", plan_text)
    print("================ PLANNER AGENT END ==================\n")

    return state | {"plan": plan_text}


# ============================================================
# AGENT 2 — SEARCHER (Tavily)
# ============================================================

def searcher_agent(state):
    print("\n================ SEARCHER AGENT START ================")

    query = state["user_query"]

    try:
        results = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=8
        )
    except Exception as e:
        print("❌ Tavily Search Error:", e)
        results = {"results": []}

    print("🔍 Search Results Retrieved!")
    print("================ SEARCHER AGENT END ==================\n")

    return state | {"search_results": results}


# ============================================================
# AGENT 3 — WRITER (Gemini)
# ============================================================

def writer_agent(state):
    print("\n================ WRITER AGENT START =================")

    plan = state["plan"]
    search_json = json.dumps(state["search_results"], indent=2)

    prompt = f"""
You are a senior research writer AI.

PLAN:
{plan}

SEARCH DATA:
{search_json}

Write a clear, well-structured research output with:

### 1. Overview  
### 2. Key Findings  
### 3. Insights  
### 4. Final Summary  

Make it crisp, factual, organized, and human-readable.
"""

    response = gemini_model.generate_content(prompt)
    final_text = response.text.strip()

    print("📝 Writer Agent Created Final Report.")
    print("================ WRITER AGENT END ==================\n")

    return state | {"final_answer": final_text}


# ============================================================
# BUILD WORKFLOW (Planner → Searcher → Writer)
# ============================================================

workflow = StateGraph(dict)

workflow.add_node("planner", planner_agent)
workflow.add_node("searcher", searcher_agent)
workflow.add_node("writer", writer_agent)

workflow.set_entry_point("planner")

workflow.add_edge("planner", "searcher")
workflow.add_edge("searcher", "writer")
workflow.add_edge("writer", END)

pipeline = workflow.compile()


# ============================================================
# RUN PIPELINE
# ============================================================

def run_pipeline(query):
    state = create_initial_state(query)
    final_state = pipeline.invoke(state)
    return final_state["final_answer"]


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    query = input("Enter your research topic: ")
    answer = run_pipeline(query)

    print("\n================ FINAL OUTPUT ================\n")
    print(answer)
