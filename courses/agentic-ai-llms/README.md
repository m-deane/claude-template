# Agentic AI & Large Language Models

## Course Overview

Build production-grade AI agent systems using modern LLM architectures. Learn to design, implement, and deploy autonomous agents that can reason, plan, use tools, and collaborate to accomplish complex tasks.

**Level:** Advanced
**Prerequisites:** Python proficiency, ML fundamentals, API experience
**Duration:** 8 modules (10-12 weeks)
**Effort:** 10-12 hours per week

## Why Agentic AI?

Traditional LLMs respond to single prompts. Agents go further—they:
- **Reason** through multi-step problems
- **Plan** sequences of actions
- **Use tools** to interact with the world
- **Remember** context across interactions
- **Collaborate** with other agents
- **Learn** from feedback and self-correct

## Learning Outcomes

By completing this course, you will:

1. **Architect** agent systems with appropriate tool sets and memory
2. **Implement** ReAct, chain-of-thought, and tree-of-thought patterns
3. **Build** multi-agent systems with orchestration and communication
4. **Integrate** RAG for grounded, factual agent responses
5. **Evaluate** agent performance with systematic benchmarks
6. **Deploy** agents to production with observability and safety guardrails

## Course Structure

| Module | Topic | Key Skills |
|--------|-------|------------|
| 0 | Foundations | Transformer review, API setup, prompt basics |
| 1 | LLM Fundamentals for Agents | Prompt engineering, system prompts, CoT |
| 2 | Tool Use & Function Calling | Tool design, error handling, security |
| 3 | Memory & Context | RAG, vector stores, conversation management |
| 4 | Planning & Reasoning | ReAct, goal decomposition, self-reflection |
| 5 | Multi-Agent Systems | Orchestration, communication, specialization |
| 6 | Evaluation & Safety | Benchmarks, guardrails, red teaming |
| 7 | Production Deployment | Observability, caching, cost optimization |

## Technology Stack

**LLM Providers:**
- Anthropic Claude (primary)
- OpenAI GPT-4
- Open-source: Llama 3, Mistral, Mixtral

**Frameworks:**
- LangChain / LangGraph
- CrewAI
- Autogen

**Infrastructure:**
- Vector stores: Chroma, Pinecone
- Observability: LangSmith, Phoenix
- Deployment: FastAPI, Docker

## Setup

```bash
# Create environment
python -m venv agent-env
source agent-env/bin/activate

# Core packages
pip install langchain langgraph langchain-anthropic langchain-openai
pip install chromadb sentence-transformers
pip install fastapi uvicorn

# Development tools
pip install jupyter pytest python-dotenv
```

## API Keys Required

```bash
# .env file
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # Optional
```

---

*"Agents are not just language models—they are systems that act in the world. Building them requires thinking about architecture, not just prompts."*
