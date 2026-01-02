"""LangGraph workflow definition for multi-agent RAG system"""
from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes import retrieve_context, generate_answer, validate_answer, regenerate_answer


def should_retry(state: AgentState) -> str:
    """Conditional edge: retry generation if validation fails
    
    Returns:
        "end" if answer is valid or max retries reached
        "retry" if answer is invalid and retries available
    """
    # If answer is valid, finish
    if state.get("is_valid", True):
        return "end"
    
    # Check retry count (max 1 retry to avoid infinite loops)
    retry_count = state.get("retry_count", 0)
    if retry_count < 1:
        return "retry"
    
    # Max retries reached, return answer anyway
    return "end"


def create_agent_graph():
    """Create and compile the multi-agent workflow graph
    
    Workflow:
    1. retrieve_context: Get relevant documents from RAG system
    2. generate_answer: Generate answer using LLM with context
    3. validate_answer: Check answer quality and relevance
    4. (conditional) regenerate_answer: Retry with stricter prompt if invalid
    
    Returns:
        Compiled LangGraph application
    """
    # Initialize the graph with our state schema
    workflow = StateGraph(AgentState)
    
    # Add agent nodes (3 agents + retry logic)
    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("generate_answer", generate_answer)
    workflow.add_node("validate_answer", validate_answer)
    workflow.add_node("regenerate_answer", regenerate_answer)
    
    # Define the workflow edges
    workflow.set_entry_point("retrieve_context")
    workflow.add_edge("retrieve_context", "generate_answer")
    workflow.add_edge("generate_answer", "validate_answer")
    
    # Conditional edge based on validation result
    workflow.add_conditional_edges(
        "validate_answer",
        should_retry,
        {
            "retry": "regenerate_answer",
            "end": END
        }
    )
    
    # After regeneration, validate again
    workflow.add_edge("regenerate_answer", "validate_answer")
    
    # Compile the graph
    app = workflow.compile()
    
    return app
