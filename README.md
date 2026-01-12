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

```
2. Set Up Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```
3. Install Dependencies
```
pip install -r requirements.txt
```
🔑 Configuration
Create a .env file in the root directory.

Add your API keys as shown below. You will need keys from OpenAI, Google AI Studio, Tavily, SerpApi, and LangSmith.

# .env file
```
# 1. LLM Providers
OPENAI_API_KEY="sk-..."
GOOGLE_API_KEY="AIzaSy..."

# 2. Search Tools
TAVILY_API_KEY="tvly-..."
SERPAPI_API_KEY="..."

# 3. LangSmith Tracing (Optional but Recommended)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="[https://api.smith.langchain.com](https://api.smith.langchain.com)"
LANGCHAIN_API_KEY="lsv2_..."
LANGCHAIN_PROJECT="Fact_Checker_Agent"
```
🏃‍♂️ Usage
Run the Streamlit application:
```
streamlit run app.py
```
How to Use
1.Select Model: Use the Sidebar to choose between OpenAI and Google Gemini.

2.Enter Query: Type a claim (e.g., "Did the Eiffel Tower catch fire recently?") or paste an Image URL for analysis.

3.View Results: The agent will display its thought process ("Using Tool: web_fact_checker") and produce a final cited response.
