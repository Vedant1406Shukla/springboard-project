# 📘 Springboard Project – AI + LangGraph + Tavily Integration

This repository contains experimentation with **LangGraph**, **LangChain**, and **Tavily Search API** to build retrieval-augmented pipelines, agent workflows, and LLM-powered applications.

It includes Python scripts demonstrating:

- 🔎 **Tavily Search API** usage  
- 🔗 **LangGraph message-passing workflows**  
- 🧠 Integrating tools into custom LLM agent pipelines  
- 🏗️ Basic agent graph construction and invocation  
- 🐍 Experiments for tool-based LLM workflows  

## 🚀 Features

### ✔ Tavily API Integration
The project demonstrates how to:

- Initialize a Tavily search client  
- Execute search queries  
- Use Tavily results inside LangGraph workflows  

### ✔ LangGraph Workflow
Includes examples of:

- Creating nodes for tools and LLMs  
- Passing messages between nodes  
- Handling mixed message types (dict + LC message objects)  
- Building directed computation graphs  

### ✔ Robust Error Handling
Due to rapid updates in LangChain & LangGraph, the project includes:

- Universal message extractor  
- Fix for `HumanMessage object is not subscriptable`  
- Fix for `tool_call_id` requirement in new LangChain versions

- ## Week -1 Milestone 
Milestone 1: Weeks 1–2 – Foundation Setup
<ul>
  <li>Set up the development environment</li>
  <li>Python environment and virtualenv</li>
  <li>Install required dependencies</li>
  <li>Design project structure and architecture</li>
  <li>Define agent responsibilities and data flow</li>
  <li>Integrate local LLM via LM Studio</li>
  <li>Configure external services (e.g., Tavily)</li>
</ul>

<img width="1900" height="842" alt="Screenshot 2025-11-21 144323" src="https://github.com/user-attachments/assets/d1c32ec7-924a-40ba-ac2c-c2234ca4c138" /> <br><br>

<img width="1896" height="1026" alt="Screenshot 2025-11-21 152550" src="https://github.com/user-attachments/assets/3607207f-15be-4588-bd91-5a82c0ddaf2c" />

## Week -2 Milestone
Milestone 2: Weeks 3–4 – Core Agent Development
<ul>
● Build functional agents <br>
● Planner Agent: break down main topic<br>
● Searcher Agent: fetch content using Tavily<br>
● Writer Agent: synthesize responses using LLM<br>
● Implement execution pipeline using LangGraph<br>
● Validate basic research loop from input to summary
</ul>  
<img width="1578" height="947" alt="image" src="https://github.com/user-attachments/assets/6d9016ef-0117-40c9-981e-599a73de8b29" /> <br>
<img width="1901" height="953" alt="image" src="https://github.com/user-attachments/assets/38061a5e-1dbd-4aec-9083-d4d6d2c0738f" />



## Week -3 Milestone
Milestone 3: Weeks 5–6 – UI and Memory Integration
<ul>
● Build user interface <br>
● Clean, ChatGPT-like design <br>
● Input prompt and result display <br>
● Connect UI to backend agent pipeline <br>
● Implement session memory <br>
● Thread tracking and continuity support<br>
</ul>
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/d76f4ee5-9bd4-49f1-a132-41a4116f4d1f" />
<br>

# Deployment URL
https://opendeepresearch.streamlit.app/






