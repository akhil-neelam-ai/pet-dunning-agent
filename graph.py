"""
LangGraph Workflow: Orchestrates the PetDunning Agent
"""
from langgraph.graph import StateGraph, END
from state import AgentState
from agents.router import router_node
from agents.negotiator import negotiator_node
from agents.extractor import extractor_node
from agents.tools import tool_executor_node


def create_petdunning_graph():
    """
    Create the LangGraph workflow

    Flow:
    1. START → router (assess risk)
    2. router → negotiator (generate initial message)
    3. [User responds]
    4. extractor → analyze user intent
    5. negotiator → generate response
    6. tool_executor → execute actions (Stripe, DB)
    7. Check if conversation complete → END or loop back
    """

    # Create graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("negotiator", negotiator_node)
    workflow.add_node("extractor", extractor_node)
    workflow.add_node("tool_executor", tool_executor_node)

    # Define flow
    workflow.set_entry_point("router")

    # Router → Negotiator (always generate initial message)
    workflow.add_edge("router", "negotiator")

    # Negotiator → END (after initial message, wait for user input)
    workflow.add_edge("negotiator", END)

    return workflow.compile()


def create_response_graph():
    """
    Create a separate graph for handling user responses
    This runs after user sends a message

    Flow:
    1. START → extractor (understand intent)
    2. extractor → negotiator (generate response)
    3. negotiator → tool_executor (execute actions if needed)
    4. tool_executor → END
    """

    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("extractor", extractor_node)
    workflow.add_node("negotiator", negotiator_node)
    workflow.add_node("tool_executor", tool_executor_node)

    # Define flow
    workflow.set_entry_point("extractor")
    workflow.add_edge("extractor", "negotiator")
    workflow.add_edge("negotiator", "tool_executor")
    workflow.add_edge("tool_executor", END)

    return workflow.compile()


# Helper function to check if conversation is complete
def is_conversation_complete(state: AgentState) -> bool:
    """
    Check if conversation has reached a terminal state
    """
    terminal_stages = ['completed', 'cancelled']
    return state.get('conversation_stage') in terminal_stages


# Helper to visualize graph structure
def get_graph_structure():
    """
    Return graph structure for visualization
    """
    return {
        'nodes': [
            {'id': 'router', 'label': 'Risk Router', 'type': 'decision'},
            {'id': 'negotiator', 'label': 'AI Negotiator', 'type': 'agent'},
            {'id': 'extractor', 'label': 'Intent Extractor', 'type': 'agent'},
            {'id': 'tool_executor', 'label': 'Tool Executor', 'type': 'action'}
        ],
        'edges': [
            {'from': 'start', 'to': 'router', 'label': 'Payment Failed'},
            {'from': 'router', 'to': 'negotiator', 'label': 'Assess Risk'},
            {'from': 'negotiator', 'to': 'user', 'label': 'Send Message'},
            {'from': 'user', 'to': 'extractor', 'label': 'Reply'},
            {'from': 'extractor', 'to': 'negotiator', 'label': 'Extract Intent'},
            {'from': 'negotiator', 'to': 'tool_executor', 'label': 'Generate Response'},
            {'from': 'tool_executor', 'to': 'end', 'label': 'Execute Action'}
        ]
    }
