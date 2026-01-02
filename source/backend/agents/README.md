# Multi-Agent Architecture Documentation

## Overview

The backend uses a **3-agent multi-agent system** orchestrated by LangGraph for intelligent question answering with quality validation.

## Agent Workflow

```
User Question
     │
     ▼
┌──────────────────────┐
│  Agent 1: Retriever  │  Searches ChromaDB for relevant documents
└──────┬───────────────┘
       │ retrieved_docs
       ▼
┌──────────────────────┐
│  Agent 2: Generator  │  Creates answer using LLM + context
└──────┬───────────────┘
       │ answer
       ▼
┌──────────────────────┐
│  Agent 3: Validator  │  Checks answer quality
└──────┬───────────────┘
       │
       ├─► VALID → Return answer
       │
       └─► INVALID → Regenerate (max 1 retry) → Validate again
```

## Agent Details

### Agent 1: Document Retriever (`retrieve_context`)
- **File**: `agents/nodes.py`
- **Purpose**: Finds relevant documents from RAG system
- **Input**: User question from state
- **Output**: Formatted documents stored in `state["retrieved_docs"]`
- **Model**: None (uses vector search only)

### Agent 2: Answer Generator (`generate_answer`)
- **File**: `agents/nodes.py`
- **Purpose**: Generates contextual answer
- **Input**: Question, retrieved documents, conversation history
- **Output**: Answer stored in `state["answer"]`
- **Model**: `gemma2:2b` (lightweight, fast)
- **Temperature**: 0.3

### Agent 3: Quality Validator (`validate_answer`)
- **File**: `agents/nodes.py`
- **Purpose**: Validates answer quality and detects hallucinations
- **Input**: Question, documents, generated answer
- **Output**: Validation result (`VALID`/`INVALID`) in `state["validation"]`
- **Model**: `gemma2:2b`
- **Temperature**: 0.1 (deterministic)

### Regeneration Logic (`regenerate_answer`)
- **Trigger**: When validator marks answer as INVALID
- **Max retries**: 1 (prevents infinite loops)
- **Approach**: Uses stricter prompt forcing document-only answers
- **Model**: `gemma2:2b`
- **Temperature**: 0.3

## State Management

The agents share state through `AgentState` (`agents/state.py`):

```python
class AgentState(TypedDict):
    messages: List[BaseMessage]       # Conversation history
    question: str                      # Current question
    retrieved_docs: List[str]          # Documents from Agent 1
    answer: str                        # Answer from Agent 2
    validation: Optional[str]          # Validation from Agent 3
    is_valid: Optional[bool]           # Validation result
    retry_count: Optional[int]         # Retry counter
```

## Graph Orchestration

**File**: `agents/graph.py`

The LangGraph workflow connects agents with conditional edges:

```python
workflow.set_entry_point("retrieve_context")
workflow.add_edge("retrieve_context", "generate_answer")
workflow.add_edge("generate_answer", "validate_answer")

# Conditional retry logic
workflow.add_conditional_edges(
    "validate_answer",
    should_retry,  # Decision function
    {
        "retry": "regenerate_answer",
        "end": END
    }
)

workflow.add_edge("regenerate_answer", "validate_answer")
```

## Model Selection

### Why Gemma2:2b?

- **Speed**: 2B parameters = much faster than Llama3 (7B)
- **Performance**: Sufficient quality for RAG tasks
- **Cost**: Lower resource usage
- **Latency**: 15-45 seconds vs 4-8 minutes with Llama3

### Alternative Models

Edit `AGENT_MODEL` in `agents/nodes.py`:

```python
# Ultra-fast (2B)
AGENT_MODEL = "gemma2:2b"  # Current

# Balanced (3B)
AGENT_MODEL = "llama3.2"
AGENT_MODEL = "phi3"

# Higher quality (7B)
AGENT_MODEL = "llama3"
```

## API Integration

### Endpoint: `/v1/ask_agent/`

**File**: `api/v1/endpoints/ask_agent.py`

```python
# Convert frontend messages to LangChain format
langchain_messages = [
    HumanMessage(content=msg.content) if msg.role == "user"
    else AIMessage(content=msg.content)
    for msg in messages.messages
]

# Create and run agent graph
agent_graph = create_agent_graph()
final_state = agent_graph.invoke({
    "messages": langchain_messages,
    "question": last_user_question,
    "retrieved_docs": [],
    "answer": "",
    "validation": None,
    "is_valid": None,
    "retry_count": 0
})

# Return answer
return {"status": "200", "message": final_state["answer"]}
```

## Benefits

1. **Better Quality**: Validation catches hallucinations
2. **Self-Correction**: Automatic retry with stricter prompts
3. **Transparency**: Clear agent traces for debugging
4. **Modularity**: Easy to add/modify agents
5. **Performance**: Optimized with lightweight model

## Debugging

### View Agent Execution

Check uvicorn logs for agent flow:

```
Vector store loaded from ../database/prod (497 documents)
INFO:     127.0.0.1:58466 - "POST /v1/ask_agent/ HTTP/1.1" 200 OK
```

### Monitor State

Add print statements in `agents/nodes.py`:

```python
def validate_answer(state: AgentState) -> AgentState:
    print(f"Validating: {state['answer'][:100]}...")
    # ... validation logic
    print(f"Result: {state['is_valid']}")
    return state
```

## Future Improvements

- [ ] Add Agent 4: Source Citation (add document references)
- [ ] Parallel validation (multiple validators)
- [ ] Specialized retrievers per school (ESILV, EMLV, IIM)
- [ ] Agent performance metrics
