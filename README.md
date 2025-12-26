# ESILV Smart Assistant

> Assistant conversationnel intelligent pour l'école d'ingénieurs ESILV utilisant la technologie RAG (Retrieval-Augmented Generation) et les modèles LLM.

## 📖 Présentation du projet

**ESILV Smart Assistant** est un chatbot intelligent conçu pour répondre aux questions des étudiants, candidats et visiteurs concernant l'école ESILV (programmes, admissions, cours, vie étudiante, etc.).

Le système combine :
- **RAG (Retrieval-Augmented Generation)** : pour des réponses factuelles basées sur la documentation officielle
- **Architecture multi-agents** : pour gérer des requêtes complexes et des interactions structurées
- **Interface moderne** : interface web intuitive pour une expérience utilisateur optimale

### Cas d'usage
- Répondre aux questions sur les programmes et admissions
- Fournir des informations sur les cours et la vie étudiante
- Collecter les coordonnées des visiteurs pour un suivi personnalisé
- Recherche sémantique dans la documentation ESILV

## 🏗️ Architecture

Le projet suit une architecture **client-serveur** moderne :

```
┌─────────────────┐         ┌──────────────────┐         ┌────────────────┐
│   Frontend      │ HTTP    │     Backend      │         │    Ollama      │
│   (Next.js)     ├────────►│   (FastAPI)      ├────────►│  (LLama3 LLM)  │
│   Port 3000     │         │   Port 8000      │         │                │
└─────────────────┘         └────────┬─────────┘         └────────────────┘
                                     │
                                     ▼
                            ┌────────────────┐
                            │   ChromaDB     │
                            │ (Vector Store) │
                            └────────────────┘
```

### Backend (FastAPI + LangChain)
- API REST pour le chatbot
- Système RAG avec ChromaDB et HuggingFace embeddings
- Intégration Ollama (Llama3) pour la génération de réponses
- Endpoints : `/v1/ask/` (chat), `/v1/add_question/` (ajout Q&A)

### Frontend (Next.js)
- Interface conversationnelle moderne
- Composants React réutilisables (Chat, SearchCard, etc.)
- Gestion d'état et hooks personnalisés
- Design responsive avec Tailwind CSS

### Base de données vectorielle
- **ChromaDB** : stockage des embeddings pour la recherche sémantique
- **Sentence Transformers** : modèle multilingue pour les embeddings français

## 🛠️ Stack technique

### Backend
- **FastAPI** : framework web moderne et performant
- **LangChain** : orchestration des modèles LLM et RAG
- **ChromaDB** : base de données vectorielle
- **Ollama** : déploiement local de Llama3
- **HuggingFace Transformers** : embeddings multilingues (`paraphrase-multilingual-MiniLM-L12-v2`)
- **Python 3.10+**

### Frontend
- **Next.js 16** : framework React avec SSR
- **React 19** : bibliothèque UI
- **TypeScript** : typage statique
- **Tailwind CSS 4** : framework CSS utilitaire
- **Radix UI** : composants accessibles
- **Framer Motion** : animations

## 📁 Structure du projet

```
LLM-GenAI_gr24/
├── source/
│   ├── backend/                 # API FastAPI
│   │   ├── api/                 # Routes et endpoints
│   │   │   └── v1/
│   │   │       └── endpoints/   # ask.py, add_question.py
│   │   ├── schemas/             # Modèles Pydantic
│   │   ├── tools/               # RAG system, Ollama chat, document loader
│   │   ├── main.py              # Point d'entrée de l'application
│   │   └── requirements.txt     # Dépendances Python
│   │
│   ├── frontend/                # Interface utilisateur
│   │   └── help-center/         # Application Next.js
│   │       ├── app/             # Pages et layouts (App Router)
│   │       ├── components/      # Composants React
│   │       ├── hooks/           # Hooks personnalisés
│   │       ├── lib/             # Utilitaires
│   │       └── types/           # Types TypeScript
│   │
│   └── database/
│       ├── prod/                # Base ChromaDB de production
│       └── samples/             # Données d'exemple (JSON)
│
└── README.md                    # Ce fichier
```

## ⚙️ Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Python 3.12** installé
- **Node.js 20+** et **npm**
- **Ollama** installé ([https://ollama.ai](https://ollama.ai))
- **Git** pour cloner le repository
- Au moins **8 GB de RAM** (pour Llama3)

## 🚀 Installation et lancement

### 1. Cloner le projet

```bash
git clone https://github.com/GuillaumeRedon/LLM-GenAI_gr24.git
cd LLM-GenAI_gr24
```

### 2. Configuration Ollama

```bash
# Démarrer le serveur Ollama (Terminal 1)
ollama serve

# Télécharger le modèle Llama3 (Terminal 2)
ollama pull llama3
```

### 3. Backend - Installation et démarrage

```bash
cd source/backend

# Créer un environnement virtuel (recommandé)
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Backend disponible** : [http://localhost:8000](http://localhost:8000)  
📚 **Documentation Swagger** : [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Frontend - Installation et démarrage

```bash
cd source/frontend/help-center

# Installer les dépendances
npm install

# Lancer l'application
npm run dev
```

✅ **Frontend disponible** : [http://localhost:3000](http://localhost:3000)

## 🔐 Variables d'environnement

### Backend (.env dans source/backend/)

```env
# Optionnel - Configuration ChromaDB ou autres services
DATABASE_PATH=../database/prod
```

### Frontend (.env.local dans source/frontend/help-center/)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📦 Scripts principaux

### Backend

```bash
# Développement avec rechargement automatique
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
npm run dev      # Mode développement (port 3000)
npm run build    # Build de production
npm start        # Serveur de production
npm run lint     # Vérification du code
```

## 🧪 Utilisation

### Poser une question au chatbot

**Endpoint** : `POST /v1/ask/`

```json
{
  "messages": [
    { "role": "user", "content": "Quels sont les programmes de l'ESILV ?" }
  ]
}
```

### Ajouter une nouvelle Q&A

**Endpoint** : `POST /v1/add_question/`

```json
{
  "titre": "Admission ESILV",
  "contenu": "Les admissions se font via Parcoursup...",
  "thematique": "Admissions",
  "ecoles": "ESILV",
  "utilisateurs": "Candidats",
  "langue": "fr"
}
```

## 📚 Bonnes pratiques

### Code
- **Backend** : respecter les conventions PEP 8 pour Python
- **Frontend** : utiliser TypeScript pour le typage fort
- **Commits** : messages clairs et descriptifs (ex : `feat: add chat history`)

### Architecture
- Séparer la logique métier dans `tools/` (backend)
- Créer des composants réutilisables (frontend)
- Utiliser les hooks personnalisés pour la logique d'état

### Performance
- Les embeddings sont générés au premier lancement (peut prendre quelques minutes)
- ChromaDB persiste automatiquement les données
- Utiliser `search_kwargs={"k": 6}` pour limiter le nombre de documents récupérés

### Sécurité
- Valider toutes les entrées utilisateur avec Pydantic (backend)
- Configurer CORS correctement en production
- Ne jamais exposer les clés API dans le code source

## 🔗 Ressources utiles

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation LangChain](https://python.langchain.com/)
- [Ollama Models](https://ollama.ai/library)
- [Next.js Documentation](https://nextjs.org/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 📄 Licence

Ce projet est réalisé dans le cadre d'un projet académique pour l'ESILV.
