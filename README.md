🕵️‍♂️ Agentic AI Fake News Detection System
A multi-modal fact-checking platform that leverages Agentic AI to verify the veracity of text-based claims and the provenance of images. Built with LangGraph for advanced LLM orchestration, the system autonomously reasons through complex queries, utilizes real-time search tools, and provides evidence-backed verdicts.

🌐 Live Demo & Access
You can access the live, deployed version of this application on Railway:
```
fakenewsagent-production.up.railway.app
```

How to use the Demo:
Configure the Model: Use the sidebar to select your preferred AI Provider (OpenAI or Google Gemini) and the specific Model (e.g., GPT-4o or Gemini 2.5 Pro).

Submit a Query: Enter a textual claim or a public URL to an image in the chat input at the bottom of the screen.

Observe the Reasoning: The system will initialize a ReAct Agent. You can watch the real-time status updates as the agent decides to use tools like web_fact_checker or reverse_image_search to gather evidence.

Review the Verdict: Once the investigation is complete, the agent will provide a structured verdict (Verified, False, Misleading, or Unproven) along with citations of the sources it discovered.

🚀 Key Features
Multi-Modal Verification: Analyzes both textual claims and image URLs for comprehensive fact-checking.

ReAct Agent Architecture: Powered by LangGraph to handle reasoning and tool execution loops.

Real-time Web Investigation: Integrated with Tavily Search for high-quality source aggregation.

Digital Forensics: Uses SerpApi (Google Lens) for reverse image searches to identify media provenance.

⚙️ Local Setup & Installation
To run this project locally, use the following bash commands:
```
Bash
# 1. Clone the repository
git clone https://github.com/your-username/Fake_news_agent.git

# 2. Navigate into the project folder
cd Fake_news_agent

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the Streamlit UI
streamlit run app.py
```
🛠️ Environment VariablesBefore running the application (locally or on Railway), ensure the following environment variables are configured:
```
VariableDescription
OPENAI_API_KEYRequired for OpenAI model support
GOOGLE_API_KEYRequired for Google Gemini model support
TAVILY_API_KEYRequired for web search capabilities
SERPAPI_API_KEYRequired for reverse image search
```
🚢 DeploymentThis project includes a Dockerfile optimized for Railway.
It uses a python:3.11-slim base image and exposes port 8501 for the Streamlit server.
The deployment automatically triggers whenever you push changes to your GitHub repository.
