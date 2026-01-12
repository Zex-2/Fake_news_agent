# 🕵️‍♂️ Agentic Fact-Checking AI

A professional-grade AI Agent designed to verify claims, debunk fake news, and perform digital forensics. Built using the **ReAct (Reason + Act)** paradigm, this tool autonomously decomposes complex queries, searches the live web, performs reverse image searches, and synthesizes evidence into a verdict.

## 🚀 Features

* **Multi-Model Intelligence:** Dynamically switch between **OpenAI (GPT-4o)** and **Google Gemini (1.5 Pro)**.
* **Live Web Verification:** Uses **Tavily AI** to fetch real-time, authoritative news sources.
* **Digital Forensics:** Integrates **SerpApi (Google Lens)** for reverse image search to detect deepfakes or miscontextualized media.
* **Streaming Interface:** Real-time token streaming via **Streamlit**.
* **Observability:** Full execution tracing via **LangSmith**.

## 🛠️ Tech Stack

* **Framework:** [LangChain](https://www.langchain.com/) & [LangGraph](https://langchain-ai.github.io/langgraph/)
* **Frontend:** [Streamlit](https://streamlit.io/)
* **LLMs:** OpenAI GPT-4o/ 4o-mini, Google Gemini 2.5 Pro / 2.5 Flash
* **Tools:** Tavily Search API, SerpApi (Google Search Results)

---

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/fact-checking-agent.git](https://github.com/your-username/fact-checking-agent.git)
cd fact-checking-agent


python3 -m venv venv
source venv/bin/activate
