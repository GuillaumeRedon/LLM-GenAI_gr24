# Frontend - Help Center Application

> Next.js interface for HelpAI chatbot with Multi-Agent backend

## 🚀 Quick Start

```bash
cd source\frontend\help-center
npm install
npm run dev
```

**Application accessible at**: http://localhost:3000

## 📋 Configuration

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🤖 Features

- **Multi-Agent Chat**: Uses `/v1/ask_agent/` endpoint with 3-agent workflow
- **Real-time conversation** with AI assistant
- **Help request management** for unanswered questions
- **Markdown support** for rich responses

## 🛠️ Stack

- Next.js 16 + React 19 + TypeScript
- Tailwind CSS 4
- Radix UI Components

## 📦 Commandes

```bash
npm run dev      # Développement
npm run build    # Build production
npm start        # Serveur production
```

---

📖 **Documentation complète** : [README principal](../../../README.md)
