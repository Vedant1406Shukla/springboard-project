# OpenDeepResearcher: Agentic LLM Research Framework

## 1. Project Title
OpenDeepResearcher – An Agentic LLM-Based Deep Research Assistant

## 2. Project Overview
OpenDeepResearcher is an AI-powered research assistant designed to autonomously conduct deep,
structured, and multi-perspective research on complex topics using Large Language Models (LLMs)
and agentic workflows.

**Problem Solved**
- Manual research is time-consuming and fragmented
- Difficult to synthesize information from multiple sources

**Objective**
- Automate planning, retrieval, analysis, and report generation

## 3. Software and Hardware Dependencies

### Software
<ul>
<li> <b>Programming Language:</b> Python 3.10+.</li>
<li>  <b>Core Frameworks:</b>
  <ul>
     <li><b>LangGraph: </b> For defining and executing multi-agent workflows.</li>
    <li><b>LangChain:</b> For LLM integration, memory handling, and tool coordination.</li>
  </ul>
</li>
<li> <b>APIs & Integration:</b>
      <ul>
        <li><b>Tavily API:</b> For real-time web search and information retrieval.</li>
        <li><b>LM Studio / Ollama:</b> To run local language models (e.g., Qwen2.5-7B-Instruct) via an OpenAI-compatible interface.</li>    
      </ul>
</li>
  <li><b>Environment Management:</b> pip / venv and Git.</li>
</ul>

### Hardware
- Minimum 8 GB RAM (16 GB recommended)
- GPU optional for faster inference

## 4. Architecture Diagram
<img width="1156" height="428" alt="image" src="https://github.com/user-attachments/assets/71d39cde-abba-4683-8cb7-cf64c2a94f39" />


## 5. Workflow
1. User enters research query
2. Planner agent creates research plan
3. Searcher agent retrieves web data
4. Writer agent synthesizes content
5. Final research report generated
<br>
<img width="1635" height="527" alt="image" src="https://github.com/user-attachments/assets/bb692b6b-0ae2-4350-8154-2938f288c89c" />


## 6. Agent Roles
- Planner: Task decomposition and planning
- Searcher: Web information retrieval
- Writer: Summarization and report writing
- Pipeline: Agent orchestration via LangGraph

## 7. Sample Demo
The user enters a research query through the interface, which is decomposed into sub-tasks by the Planner Agent. Relevant information is fetched from the web using the Searcher Agent, and the Writer Agent synthesizes the data into a structured research report displayed to the user.

<img width="1919" height="1079" alt="Screenshot 2025-12-15 183009" src="https://github.com/user-attachments/assets/7715253f-e04a-41ee-93aa-66f033e0545f" />


## 8. Outputs
- Structured research reports
- Summarized insights
- Context-aware responses
<img width="1919" height="1023" alt="image" src="https://github.com/user-attachments/assets/6a7dac7f-5f45-4afb-aaa2-d156cd92d520" />


## 9. Limitations
- Dependent on LLM quality
- Web data accuracy varies
- Performance limited on low-resource systems

## 10. Future Enhancements
- PDF/Markdown export
- Citation validation
- Multi-language support
- Cloud deployment

## 11. Deployed Project Link
https://opendeepresearch.streamlit.app/
