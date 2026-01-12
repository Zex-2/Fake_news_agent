# backend/graph.py
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import tools_condition, ToolNode
from backend.state import AgentState
from backend.agent import agent_node, tools

def build_graph():
    """
    Constructs and compiles the LangGraph state machine.
    """
    workflow = StateGraph(AgentState)

    # Add the nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))

    # Define the entry point
    workflow.add_edge(START, "agent")

    # Define the conditional routing
    # 'tools_condition' is a prebuilt helper that checks for 'tool_calls' in the last message
    workflow.add_conditional_edges(
        "agent",
        tools_condition,
    )

    # Define the return loop from tools back to the agent
    workflow.add_edge("tools", "agent")

    # Compile the graph
    # In a production app, we would pass a 'checkpointer' here to enable memory persistence
    # across different user sessions.
    return workflow.compile()

# Initialize the application instance
app = build_graph()