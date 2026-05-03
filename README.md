# LangChain Academy - Introduction to LangChain (Python)

**Course Completion Project** | Completely Free Setup with Local Models

---

## 📚 Course Overview

This repository documents the completion of **LangChain Academy's Introduction to LangChain (Python)** course. The course provides hands-on learning across three comprehensive modules, building progressively from foundational concepts to production-ready agents.

### Course Modules Completed

- **Module 1: Create Agent** - Foundational models, tools, memory, and multimodal messages
- **Module 2: Advanced Agent** - Model Context Protocol (MCP), context management, and multi-agent systems
- **Module 3: Production-Ready Agent** - Middleware, long conversation handling, and human-in-the-loop workflows

---

## 🚀 Setup & Technology Stack

### Models Used

**Language Model:** Mistral (via Ollama)
- **Why Mistral:** Optimal balance of speed, quality, and tool support for learning
- **Provider:** Ollama (free, runs locally on CPU)
- **Cost:** $0 (completely free alternative to proprietary APIs)

**Embedding Model:** Mistral Embeddings (via Ollama)
- Converts text to vector representations for semantic search
- Free alternative to OpenAI's text-embedding-3-large

### Supporting Services

| Service | Purpose | Cost | Status |
|---------|---------|------|--------|
| **Ollama** | Local LLM runtime | Free | ✅ Used |
| **Tavily Search** | Web search for agents | Free tier | ✅ Used |
| **LangChain** | Agent/chain framework | Free | ✅ Used |
| **LanGraph** | Agent orchestration & state | Free | ✅ Used |

---

## 💻 Installation & Setup

### Prerequisites

- Python >= 3.12
- 20+ GB free disk space
- Ollama installed (https://ollama.ai)
- Git

### Quick Start

```bash
# 1. Clone the course repository
git clone --depth 1 https://github.com/langchain-ai/lca-lc-foundations.git
cd lca-lc-foundations

# 2. Install Ollama and download Mistral
ollama pull mistral

# 3. Create environment file
cp example.env .env

# 4. Add your Tavily API key to .env
# Get free key from: https://tavily.com
TAVILY_API_KEY='your-key-here'

# 5. Install dependencies
uv sync

# 6. Run Ollama (Terminal 1 - keep running)
ollama serve

# 7. Start Jupyter (Terminal 2)
uv run jupyter lab
```

### Environment File Template

```env
# Using Ollama (free, local)
OPENAI_API_KEY='placeholder'

# Search API (free tier from tavily.com)
TAVILY_API_KEY='your-tavily-api-key-here'

# Optional (not required for course)
ANTHROPIC_API_KEY=''
GOOGLE_API_KEY=''
LANGSMITH_API_KEY=''
LANGSMITH_TRACING=false
```

---

**)All course notebooks were modified to use Ollama instead of proprietary APIs**

## 🎯 Course Projects Completed

### Module 1: Personal Chef Agent
- Built an agent that understands recipes
- Integrated tools for ingredient lookup
- Implemented short-term conversation memory

### Module 2: Wedding Planner Agent
- Created multi-agent system
- Implemented MCP (Model Context Protocol)
- Managed complex state across multiple agents

### Module 3: Email Assistant
- Built production-ready agent with middleware
- Implemented long conversation management
- Added human-in-the-loop approval system

### Module 3: Picnic Planner Agent
- Added a Groq-powered LangGraph agent for weather-aware picnic planning
- Uses Open-Meteo's public weather API, so no weather API key is required
- Recommends indoor vs. outdoor picnic plans with forecast, venue ideas, packing list, and backup plan

Run locally:

```bash
cd module-3
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

GROQ_API_KEY="your-groq-key" LANGSMITH_TRACING=false langgraph dev --config langgraph.json --port 2025
```

In Agent Chat, use:

```text
Deployment URL: http://localhost:2025
Assistant / Graph ID: picnic_agent
LangSmith API Key: leave blank for local
```

Example prompts:

```text
Plan a picnic in Chicago tomorrow for 4 people.
Should I do an indoor or outdoor picnic in Austin this Saturday?
```

---

## 📊 Performance Metrics

### Model Comparison (Tested on This Course)

| Metric | Mistral | Phi | Llama2 |
|--------|---------|-----|--------|
| **Speed** | ~20-30 tokens/sec | ~40-50 tokens/sec | ~10-15 tokens/sec |
| **Quality** | Excellent | Good | Excellent |
| **Size** | 4 GB | 2.6 GB | 3.8 GB |
| **Tools Support** | ✅ Yes | ✅ Yes | ❌ No |
| **Best For** | Learning (recommended) | Quick tests | High quality |

**Recommendation:** Mistral is optimal for this course — balances learning quality with reasonable speed.

---

## 🛠️ Troubleshooting

### Connection Error: "Cannot connect to Ollama"

```bash
# Make sure Ollama is running in a separate terminal
ollama serve

# Or check if it's running
curl http://localhost:11434/api/generate -d '{"model":"mistral","prompt":"test"}'
```

### Model Not Found Error

```bash
# Download the model
ollama pull mistral

# List available models
ollama list
```

### Slow Responses

Switch to a faster model:
```python
# Use Phi for speed
model = ChatOllama(model="phi")
```

### Tool Support Error with Llama2

**Issue:** "llama2 does not support tools"  
**Solution:** Use Mistral or Phi instead (both support function calling)

```python
# ❌ Don't use llama2 with agents
# model = ChatOllama(model="llama2")

# ✅ Use mistral or phi
model = ChatOllama(model="mistral")
```

---

## 📚 Learning Resources

### Official Documentation
- [LangChain Docs](https://python.langchain.com)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Ollama Documentation](https://ollama.ai)

### Course Materials
- [LangChain Academy](https://academy.langchain.com)
- [GitHub Repository](https://github.com/langchain-ai/lca-lc-foundations)

### Key Concepts Learned
- LLM Fundamentals and prompting
- Tool/function calling and agents
- Conversation memory and state management
- Multi-agent systems and coordination
- Production patterns (middleware, checkpoints, HITL)

---

## 💡 Cost Breakdown

### This Setup vs. Cloud APIs

| Component | Cloud (OpenAI) | This Setup (Ollama) | Savings |
|-----------|---|---|---|
| GPT-4.5-nano calls | $0.30/1M tokens | Free | 100% |
| Embeddings | $0.02/1M tokens | Free | 100% |
| Search (Tavily) | Free tier | Free tier | - |
| **Total for course** | ~$5-20 | **$0** | **$5-20** |

**Total spent:** $0 ✅

---

## 📁 Project Structure

```
lca-lc-foundations/
├── notebooks/
│   ├── module-1/          # Create Agent
│   │   ├── lesson-1.ipynb
│   │   ├── lesson-2.ipynb
│   │   └── project.ipynb
│   ├── module-2/          # Advanced Agent
│   │   ├── lesson-1.ipynb
│   │   ├── lesson-2.ipynb
│   │   └── project.ipynb
│   └── module-3/          # Production-Ready
│       ├── lesson-1.ipynb
│       ├── lesson-2.ipynb
│       └── project.ipynb
├── .env                   # API keys (excluded from git)
├── pyproject.toml         # Python dependencies
└── env_utils.py          # Setup verification script
```

---

## 📖 Course Credits

**Course:** Introduction to LangChain (Python)  
**Provider:** LangChain Academy  
**Repository:** https://github.com/langchain-ai/lca-lc-foundations  
**Completed:** 2026

---
**Happy Learning!** 🚀

