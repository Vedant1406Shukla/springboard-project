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

<img width="1900" height="842" alt="Screenshot 2025-11-21 144323" src="https://github.com/user-attachments/assets/d1c32ec7-924a-40ba-ac2c-c2234ca4c138" /> <br><br>

<img width="1896" height="1026" alt="Screenshot 2025-11-21 152550" src="https://github.com/user-attachments/assets/3607207f-15be-4588-bd91-5a82c0ddaf2c" />

