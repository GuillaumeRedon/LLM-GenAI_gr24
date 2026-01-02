# ESILV Smart Assistant

> Intelligent conversational assistant for the ESILV engineering school using RAG (Retrieval-Augmented Generation) technology and LLM models.

## 📖 Project Overview

**ESILV Smart Assistant** is an intelligent chatbot designed to answer questions from students, candidates, and visitors about ESILV school (programs, admissions, courses, student life, etc.). It is build to assist the HelpCenter, a website that stores frequently asked questions. When a topic cannot be found using the existing hard-matching system, the user can use the Smart Assistant to get the answer it seeks. 

The system combines:
- **RAG (Retrieval-Augmented Generation)**: for factual answers based on official documentation
- **Multi-agent architecture**: to handle complex queries and structured interactions
- **Modern interface**: intuitive web interface for optimal user experience

### Use Cases
- Answer questions about programs and admissions
- Provide information on courses and student life
- Collect visitor details for personalized follow-up
- Semantic search in ESILV documentation

## 🏗️ Architecture

The project follows a modern **client-server** architecture with **multi-agent system**:

```
┌─────────────────┐         ┌──────────────────────────────┐         ┌────────────────┐
│   Frontend      │ HTTP    │     Backend (Multi-Agent)    │         │    Ollama      │
│   (Next.js)     ├────────►│   (FastAPI + LangGraph)      ├────────►│  (Gemma2:2b)   │
│   Port 3000     │         │   Port 8000                  │         │                │
└─────────────────┘         └────────┬─────────────────────┘         └────────────────┘
                                     │
                                     ▼
                            ┌────────────────┐
                            │   ChromaDB     │
                            │ (Vector Store) │
                            └────────────────┘

Multi-Agent Workflow:
  Agent 1: Document Retriever → Agent 2: Answer Generator → Agent 3: Quality Validator
```

### Backend (FastAPI + LangChain + LangGraph)
- REST API for the chatbot
- **Multi-agent RAG system** with 3 specialized agents
- RAG with ChromaDB and HuggingFace embeddings
- Ollama (Gemma2:2b) integration for fast response generation
- Endpoints: `/v1/ask_agent/` (multi-agent), `/v1/add_question/` (add Q&A)

### Frontend (Next.js)
- Modern conversational interface
- Reusable React components (Chat, SearchCard, etc.)
- State management and custom hooks
- Responsive design with Tailwind CSS

### Vector Database
- **ChromaDB**: storage of embeddings for semantic search
- **Sentence Transformers**: multilingual model for French embeddings

## 🛠️ Technical Stack

### Backend
- **FastAPI**: modern and performant web framework
- **LangChain**: orchestration of LLM and RAG models
- **LangGraph**: multi-agent workflow orchestration
- **ChromaDB**: vector database
- **Ollama**: local deployment of LLMs (Gemma2:2b for agents)
- **HuggingFace Transformers**: multilingual embeddings (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Python 3.10+**

### Frontend
- **Next.js 16**: React framework with SSR
- **React 19**: UI library
- **TypeScript**: static typing
- **Tailwind CSS 4**: utility CSS framework
- **Radix UI**: accessible components
- **Framer Motion**: animations

## 📁 Project Structure

```
LLM-GenAI_gr24/
├── source/
│   ├── backend/                 # FastAPI API
│   │   ├── agents/              # Multi-agent system (LangGraph)
│   │   │   ├── state.py         # Agent state schema
│   │   │   ├── nodes.py         # Agent node functions
│   │   │   ├── graph.py         # Workflow orchestration
│   │   │   ├── tools.py         # Agent tools (RAG wrapper)
│   │   │   └── README.md        # Agents Orchestration README
│   │   ├── api/                 # Routes and endpoints
│   │   │   └── v1/
│   │   │       └── endpoints/   # ask.py, ask_agent.py, add_question.py
│   │   ├── schemas/             # Pydantic models
│   │   ├── tools/               # RAG system, Ollama chat, document loader
│   │   ├── main.py              # Application entry point
│   │   ├── requirements.txt     # Python dependencies
│   │   └── README.md            # Backend README
│   │
│   │
│   ├── frontend/                # User interface
│   │   └── help-center/         # Next.js application
│   │       ├── app/             # Pages and layouts (App Router)
│   │       ├── components/      # React components
│   │       ├── hooks/           # Custom hooks
│   │       ├── lib/             # Utilities
│   │       ├── types/           # TypeScript types
│   │       └── README.md        # Frontend README
│   │
│   └── database/
│       ├── prod/                # Production ChromaDB database
│       └── samples/             # Sample data (JSON)
│
└── README.md                    # This file
```

## ⚙️ Prerequisites

Before starting, make sure you have:

- **Python 3.12** installed
- **Node.js 20+** and **npm**
- **Ollama** installed ([https://ollama.ai](https://ollama.ai))
- **Git** to clone the repository

## 🚀 Installation and Launch

### 1. Clone the Project

```bash
git clone https://github.com/GuillaumeRedon/LLM-GenAI_gr24.git
cd LLM-GenAI_gr24
```

### 2. Ollama Configuration

```bash
# Start the Ollama server (Terminal 1)
ollama serve

# Download the models (Terminal 2)
ollama pull gemma2:2b      # For multi-agent system (faster)
```

### 3. Backend - Installation and Startup

```bash
cd source/backend

# Create a virtual environment (recommended)
python3.12 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate.ps1     # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Backend available**: [http://localhost:8000](http://localhost:8000)  
📚 **Swagger documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Frontend - Installation and Startup

```bash
cd source/frontend/help-center

# Install dependencies
npm install

# Start the application
npm run dev
```

✅ **Frontend available**: [http://localhost:3000](http://localhost:3000)

## 🔐 Environment Variables

### Backend (.env in source/backend/)

```env
# Optional - ChromaDB configuration or other services
DATABASE_PATH=../database/prod
```

### Frontend (.env.local in source/frontend/help-center/)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📦 Main Scripts

### Backend

```bash
# Development with automatic reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
npm run dev      # Development mode (port 3000)
npm run build    # Production build
npm start        # Production server
npm run lint     # Code verification
```

## 🧪 Usage

### Ask a Question to the Chatbot

**Multi-Agent Endpoint**: `POST /v1/ask_agent/`

```json
{
  "messages": [
    { "role": "user", "content": "What are the ESILV programs?" }
  ]
}
```

### Add a New Q&A

**Endpoint**: `POST /v1/add_question/`

```json
{
  "titre": "ESILV Admission",
  "contenu": "Admissions are done through Parcoursup...",
  "thematique": "Admissions",
  "ecoles": "ESILV",
  "utilisateurs": "Candidats",
  "langue": "fr"
}
```

## 📚 Best Practices

### Code
- **Backend**: follow PEP 8 conventions for Python
- **Frontend**: use TypeScript for strong typing
- **Commits**: clear and descriptive messages (e.g., `feat: add chat history`)

### Architecture
- Separate business logic in `tools/` (backend)
- Create reusable components (frontend)
- Use custom hooks for state logic

### Performance
- Embeddings are generated on first launch (may take a few minutes)
- ChromaDB automatically persists data
- Use `search_kwargs={"k": 6}` to limit the number of retrieved documents

### Security
- Validate all user inputs with Pydantic (backend)
- Configure CORS correctly in production
- Never expose API keys in source code

## 🔗 Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Models](https://ollama.ai/library)
- [Next.js Documentation](https://nextjs.org/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 📄 License

This project is carried out as part of an academic project for ESILV.