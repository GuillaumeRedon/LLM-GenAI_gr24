# Backend - RAG System API

> API FastAPI avec système RAG (LangChain + ChromaDB + Ollama Llama3)

## 🚀 Démarrage rapide

```bash
cd source/backend

# Terminal 1 - Ollama
ollama serve
ollama pull llama3

# Terminal 2 - Backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API accessible sur** : http://localhost:8000  
**Documentation** : http://localhost:8000/docs

## 📋 Endpoints

- `POST /v1/ask/` - Chat avec l'assistant
- `POST /v1/add_question/` - Ajouter une Q&A

## 🛠️ Stack

- FastAPI + LangChain + ChromaDB
- Ollama (Llama3 local)
- HuggingFace Embeddings

---

📖 **Documentation complète** : [README principal](../../README.md)
