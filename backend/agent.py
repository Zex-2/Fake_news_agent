# backend/agent.py

from dotenv import load_dotenv
load_dotenv()
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from langchain_core.runnables import RunnableConfig  # [FIX] Added missing import
from backend.state import AgentState
from backend.state import get_web_search_tool
from backend.tools import reverse_image_search

# 1. Define Tools Globally (so graph.py can access them)
#    Note: Do not call reverse_image_search() with (), just pass the function name.
tools = [get_web_search_tool(), reverse_image_search]

# 2. Define System Prompt
SYSTEM_PROMPT = """You are an expert Fact-Checking Agent specializing in digital forensics. 
Your goal is to verify user claims and analyze media for authenticity.

PROTOCOL:
1. Decompose the user's input into verifiable facts.
2. Investigate using `web_fact_checker` and `reverse_image_search`.
3. Synthesize evidence and provide a clear verdict: "Verified", "False", "Misleading", or "Unproven".
4. ALWAYS cite your sources.
"""

def agent_node(state: AgentState, config: RunnableConfig):
    """
    The primary reasoning node. 
    Accepts 'config' to dynamically switch between OpenAI and Gemini.
    """
    # [FIX] 1. Get configuration from the user session
    configuration = config.get("configurable", {})
    selected_provider = configuration.get("model_provider", "openai")
    selected_model = configuration.get("model_name", "gpt-4o")

    # [FIX] 2. Initialize the LLM *inside* the node based on selection
    if selected_provider == "gemini":
        # Fallback to a valid Gemini model if the name implies GPT
        if "gpt" in selected_model:
            selected_model = "gemini-2.5-pro"
            
        llm = ChatGoogleGenerativeAI(
            model=selected_model,
            temperature=0,
            convert_system_message_to_human=True,
            api_key=os.environ.get("GOOGLE_API_KEY")
        )
    else:
        # Default to OpenAI
        llm = ChatOpenAI(
            model=selected_model, 
            temperature=0, 
            streaming=True,
            api_key=os.environ.get("OPENAI_API_KEY")
        )

    # [FIX] 3. Bind tools to this specific LLM instance
    llm_with_tools = llm.bind_tools(tools)

    # 4. Prepare the prompt
    messages = state['messages']
    sys_msg = SystemMessage(content=SYSTEM_PROMPT)
    prompt_messages = [sys_msg] + messages
    
    # 5. Invoke
    response = llm_with_tools.invoke(prompt_messages)
    
    return {"messages": [response]}