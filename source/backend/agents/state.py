"""Agent state schema for LangGraph workflow"""
from typing import List, TypedDict, Annotated, Optional
from operator import add
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """State shared across all agent nodes in the workflow"""
    
    # Conversation messages (user + assistant history)
    messages: Annotated[List[BaseMessage], add]
    
    # Current question to answer
    question: str
    
    # Retrieved documents from RAG
    retrieved_docs: List[str]
    
    # Generated answer
    answer: str
    
    # Validation result from validator agent
    validation: Optional[str]
    
    # Is the answer valid?
    is_valid: Optional[bool]
    
    # Retry counter to prevent infinite loops
    retry_count: Optional[int]
