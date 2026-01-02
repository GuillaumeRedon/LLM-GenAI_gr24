"""Multi-agent endpoint using LangGraph for question answering"""
from fastapi import APIRouter
from schemas.message import MessageList
from agents.graph import create_agent_graph
from langchain_core.messages import HumanMessage, AIMessage

router = APIRouter()


@router.post("/", summary="Ask something to the AI using multi-agent system")
async def ask_agent(messages: MessageList):
    """
    Multi-agent question answering endpoint using LangGraph.
    
    This endpoint uses a multi-agent workflow:
    1. Retrieve Context Agent: Finds relevant documents from RAG
    2. Generate Answer Agent: Creates response using LLM + context
    3. Validate Answer Agent: Checks answer quality and triggers retry if needed
    
    Args:
        messages: Conversation history with user messages
        
    Returns:
        Response with status and generated answer
    """
    try:
        # Extract the last user question
        user_messages = [msg for msg in messages.messages if msg.role == "user"]
        if not user_messages:
            return {"status": "400", "message": "Aucune question utilisateur trouvée"}
        
        last_user_question = user_messages[-1].content
        
        # Convert message history to LangChain format
        langchain_messages = []
        for msg in messages.messages:
            if msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "agent":
                langchain_messages.append(AIMessage(content=msg.content))
        
        # Create the agent graph
        agent_graph = create_agent_graph()
        
        # Prepare initial state
        initial_state = {
            "messages": langchain_messages,
            "question": last_user_question,
            "retrieved_docs": [],
            "answer": "",
            "validation": None,
            "is_valid": None,
            "retry_count": 0
        }
        
        # Execute the agent workflow
        final_state = agent_graph.invoke(initial_state)
        
        # Extract the answer from final state
        answer = final_state.get("answer", "Erreur lors de la génération de la réponse")
        
        return {"status": "200", "message": answer}
    
    except Exception as e:
        return {"status": "500", "message": f"Error: {str(e)}"}
