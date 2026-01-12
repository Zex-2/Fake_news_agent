# backend/state.py
import operator
from typing import Annotated, TypedDict, Union, List
from langchain_core.messages import BaseMessage, AnyMessage
from langgraph.graph.message import add_messages
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
class AgentState(TypedDict):
    """
    The persistent state of the agent workflow.
    
    Attributes:
        messages (list): A sequence of messages (Human, AI, Tool) representing the conversation history.
                         The Annotated wrapper with `add_messages` ensures append-only behavior.
    """
    messages: Annotated[List[AnyMessage], add_messages]
    
    # We can add additional state keys here if needed, e.g.:
    # research_summary: str  (to hold a running summary of findings)
    # steps_taken: int       (to enforce a custom recursion limit)
    # backend/tools.py

def get_web_search_tool():
    """
    Factory function to create the Tavily search tool.
    
    Configuration:
    - max_results=5: Retrieves a broad set of perspectives to avoid single-source bias.
    - search_depth="advanced": Ensures retrieval of high-quality content, not just headlines.
    - include_answer=True: Requests Tavily's own LLM to summarize the findings initially.
    - include_raw_content=True: vital for allowing the Agent to read the actual article text.
    """
    return TavilySearch(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=False, # We handle images via SerpApi
        #name="web_fact_checker",
        #description="Useful for verifying factual claims, news events, and general knowledge. "
                  #  "Input should be a specific search query."
                    
    )