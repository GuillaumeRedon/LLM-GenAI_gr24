"""Agent node functions for the LangGraph workflow"""
from agents.state import AgentState
from agents.tools import RAGRetrieverTool
from tools.ollamaChat import create_ollama_chat
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage


# Lightweight model for faster agent performance
AGENT_MODEL = "gemma2:2b"


def retrieve_context(state: AgentState) -> AgentState:
    """Node: Retrieve relevant documents from RAG system
    
    This agent node uses the RAG retriever to find documents
    relevant to the user's question.
    """
    question = state["question"]
    
    # Initialize RAG retriever tool
    rag_tool = RAGRetrieverTool()
    
    # Retrieve documents
    docs = rag_tool.retrieve(question, k=6)
    
    # Format documents for context
    formatted_docs = rag_tool.format_docs(docs)
    
    # Store in state
    state["retrieved_docs"] = [formatted_docs]
    
    return state


def generate_answer(state: AgentState) -> AgentState:
    """Node: Generate answer using LLM with retrieved context
    
    This agent node takes the retrieved documents and conversation
    history to generate a contextual answer.
    """
    question = state["question"]
    retrieved_docs = state.get("retrieved_docs", [])
    messages = state.get("messages", [])
    
    # Format conversation history
    conversation_history = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            conversation_history.append(f"Utilisateur: {msg.content}")
        elif isinstance(msg, AIMessage):
            conversation_history.append(f"Assistant: {msg.content}")
    
    conversation_str = "\n".join(conversation_history)
    
    # Context from retrieved documents
    context = retrieved_docs[0] if retrieved_docs else "Aucun document trouvé."
    
    llm = create_ollama_chat(model=AGENT_MODEL, temperature=0.3)
    
    # Prompt template
    template = """Tu es un assistant virtuel pour une école. Tu dois répondre à la dernière question de l'utilisateur en t'appuyant sur:
1. Les documents de la base de connaissances ci-dessous
2. L'historique de la conversation pour comprendre le contexte

RÈGLES IMPORTANTES:
- Utilise les informations des documents pour répondre, même si la formulation de la question n'est pas exactement la même que dans les documents
- Si les documents contiennent des informations pertinentes qui peuvent aider à répondre, utilise-les pour construire ta réponse
- Sois clair et pédagogique dans tes explications
- Si vraiment AUCUNE information dans les documents ne peut aider à répondre (par exemple une question sur la météo), dis alors : "Je n'ai pas d'information sur ce sujet dans ma base de connaissances."
- Ne réponds QU'À la dernière question posée
- Utilise l'historique pour comprendre le contexte de la conversation

=== DOCUMENTS DE LA BASE DE CONNAISSANCES ===
{context}

=== HISTORIQUE DE LA CONVERSATION ===
{conversation_history}

=== DERNIÈRE QUESTION À RÉPONDRE ===
{question}

Réponse de l'assistant:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create chain
    chain = prompt | llm
    
    # Generate response
    response = chain.invoke({
        "context": context,
        "conversation_history": conversation_str,
        "question": question
    })
    # Store answer
    state["answer"] = response.content if hasattr(response, 'content') else str(response)
    
    return state


def validate_answer(state: AgentState) -> AgentState:
    """Node: Validate answer quality and relevance
    
    This agent checks if the generated answer:
    1. Uses information from retrieved documents
    2. Answers the actual question
    3. Doesn't hallucinate
    """
    question = state["question"]
    answer = state["answer"]
    retrieved_docs = state.get("retrieved_docs", [])
    
    llm = create_ollama_chat(model=AGENT_MODEL, temperature=0.1)
    
    validation_template = """Tu es un validateur d'IA. Analyse si la réponse est de bonne qualité.

QUESTION: {question}

DOCUMENTS DISPONIBLES:
{context}

RÉPONSE GÉNÉRÉE:
{answer}

Évalue la réponse selon ces critères:
1. La réponse utilise-t-elle les informations des documents? (OUI/NON)
2. La réponse répond-elle vraiment à la question? (OUI/NON)
3. La réponse contient-elle des informations inventées non présentes dans les documents? (OUI/NON)

Réponds UNIQUEMENT par: VALID ou INVALID suivi d'une raison courte.
Format: VALID: [raison] ou INVALID: [raison]"""
    
    prompt = ChatPromptTemplate.from_template(validation_template)
    chain = prompt | llm
    
    validation_result = chain.invoke({
        "question": question,
        "context": retrieved_docs[0] if retrieved_docs else "Aucun document",
        "answer": answer
    })
    
    result_text = validation_result.content if hasattr(validation_result, 'content') else str(validation_result)
    
    # Store validation result
    state["validation"] = result_text
    state["is_valid"] = result_text.strip().startswith("VALID")
    
    print(f"🔍 Validation result: {result_text[:100]}...")
    
    return state


def regenerate_answer(state: AgentState) -> AgentState:
    """Node: Regenerate answer with stricter prompt after validation failure
    
    This agent is called when validation fails, using a more
    strict prompt to force document-based answers.
    """
    question = state["question"]
    retrieved_docs = state.get("retrieved_docs", [])
    validation_reason = state.get("validation", "")
    
    llm = create_ollama_chat(model=AGENT_MODEL, temperature=0.3)
    
    strict_template = """ATTENTION: Ta réponse précédente a été rejetée pour: {validation_reason}

Tu DOIS répondre en utilisant UNIQUEMENT les informations ci-dessous.
Si les documents ne contiennent pas d\'information pour répondre, dis clairement:
"Je n\'ai pas d\'information sur ce sujet dans ma base de connaissances."

DOCUMENTS:
{context}

QUESTION:
{question}

Réponse (basée UNIQUEMENT sur les documents):"""
    
    prompt = ChatPromptTemplate.from_template(strict_template)
    chain = prompt | llm
    
    response = chain.invoke({
        "context": retrieved_docs[0] if retrieved_docs else "",
        "question": question,
        "validation_reason": validation_reason
    })
    
    state["answer"] = response.content if hasattr(response, 'content') else str(response)
    
    return state
