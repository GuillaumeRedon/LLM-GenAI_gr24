# Backend - Multi-Agent RAG System API

> FastAPI API with Multi-Agent RAG system (LangChain + LangGraph + ChromaDB + Ollama)

## 🚀 Quick Start

```bash
cd source/backend

# Terminal 1 - Ollama
ollama serve
ollama pull gemma2:2b      # For multi-agent system (faster)

# Terminal 2 - Backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API accessible at**: http://localhost:8000  
**Documentation**: http://localhost:8000/docs

## 📋 Endpoints

- `POST /v1/ask_agent/` - **Multi-agent chat** (3 agents: Retriever → Generator → Validator)
- `POST /v1/ask/` - Legacy single-chain chat
- `POST /v1/add_question/` - Add a Q&A to knowledge base

## 🤖 Multi-Agent Architecture

**Workflow**: 
1. **Agent 1 (Retriever)**: Searches ChromaDB for relevant documents
2. **Agent 2 (Generator)**: Creates answer using LLM + context
3. **Agent 3 (Validator)**: Checks answer quality and triggers retry if needed

**Benefits**:
- Better answer quality through validation
- Automatic hallucination detection
- Self-correction with retry mechanism

## 🛠️ Stack

- FastAPI + LangChain + LangGraph
- ChromaDB (Vector Store)
- Ollama (Gemma2:2b for agents, Llama3 for legacy)
- HuggingFace Embeddings

---

📖 **Complete documentation**: [Main README](../../README.md)
