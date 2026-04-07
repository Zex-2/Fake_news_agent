# app.py
import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import HumanMessage
from backend.graph import app as graph_app

# 1. Page Configuration
st.set_page_config(
    page_title="Agentic Fact Checker",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# Custom CSS for chat interface
st.markdown("""
<style>
   .stChatMessage {
        background-color: #565756; 
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🕵️‍♂️ Agentic AI Fake News Detection")
st.markdown("""
**System Architecture:** ReAct Agent (LangGraph) | **Tools:** Tavily (Web), SerpApi (Vision)
Check the veracity of claims or image URLs below.
""")
with st.sidebar:
    st.header("⚙️ Model Configuration")
    
    # Select Provider
    provider = st.radio(
        "Select AI Provider",
        ("OpenAI", "Google Gemini"),
        index=0
    )
    
    # Dynamic Model Options
    if provider == "OpenAI":
        model_options = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
        provider_key = "openai"
    else:
        model_options = ["gemini-2.5-pro", "gemini-2.5-flash"]
        provider_key = "gemini"
        
    selected_model = st.selectbox("Select Model", model_options)
    
    st.divider()
# 2. Session State Management
# We need to persist the chat history across Streamlit reruns.
if "messages" not in st.session_state:
    st.session_state.messages =[]

# 3. Render Historical Messages
# This loop redraws the chat history every time the script runs.
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# 4. Input Handling
# We accept both text and image URLs.
query = st.chat_input("Enter a claim (e.g., 'The Eiffel Tower is on fire') or an Image URL...")

# 5. The Async Execution Logic
async def run_agent_stream(user_input, provider_key, model_name):
    """
    Executes the agent workflow and streams updates to the Streamlit UI.
    """
    # Create the HumanMessage object
    input_message = HumanMessage(content=user_input)
    
    # Immediately render the user's message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add to history
    st.session_state.messages.append(input_message)

    # Prepare the Assistant's message container
    with st.chat_message("assistant"):
        # We use a status container to show tool usage (searching, analyzing)
        status_container = st.status("Initializing Agent...", expanded=True)
        # We use an empty container to stream the text tokens
        text_container = st.empty()
        full_response = ""

        run_config = {
            "configurable": {
                "thread_id": "1",
                "model_provider": provider_key,
                "model_name": model_name
            }
        }
        async for event in graph_app.astream_events(
            {"messages": st.session_state.messages},
            config=run_config,  # <--- PASS CONFIG HERE
            version="v1"
        ):
       
            kind = event["event"]
            name = event["name"]
            data = event["data"]
            
            # CASE A: The LLM is generating text (Streaming tokens)
            if kind == "on_chat_model_stream":
                if event.get("metadata", {}).get("langgraph_node") == "agent":
                    chunk = data.get("chunk")
                    if chunk:
                        content = chunk.content
                        
                        # [FIX START] Handle different content types
                        text_to_append = ""
                        
                        if isinstance(content, str):
                            # OpenAI returns string
                            text_to_append = content
                        elif isinstance(content, list):
                            # Gemini returns list of objects (Text/Tool calls)
                            for item in content:
                                if isinstance(item, dict) and 'text' in item:
                                     # Extract 'text' field if available
                                    text_to_append += item['text']
                                elif isinstance(item, str):
                                    # Sometimes list contains strings directly
                                    text_to_append += item
                        
                        # Only append and update UI if we found text
                        if text_to_append:
                            full_response += text_to_append
                            text_container.markdown(full_response + "▌")
            # CASE B: A Tool is Starting
            elif kind == "on_tool_start":
                status_container.write(f"🛠️ **Activating Tool:** `{name}`")
                with status_container:
                    st.json(data.get("input")) # Show the query inputs
            
            # CASE C: A Tool has Finished
            elif kind == "on_tool_end":
                status_container.write(f"✅ **Tool Completed:** `{name}`")
                # We optionally show the output, or keep it collapsed to avoid clutter
                # with status_container:
                #     st.code(str(data.get("output"))[:500]) 

        # Finalize the UI
        status_container.update(label="Investigation Complete", state="complete", expanded=False)
        text_container.markdown(full_response)
        
        # Add the final response to session state so it persists
        st.session_state.messages.append(HumanMessage(content=full_response))

# 6. Bridge Sync to Async
# Streamlit is synchronous, so we use asyncio.run() to enter the async world.
if query:
    asyncio.run(run_agent_stream(query, provider_key, selected_model))