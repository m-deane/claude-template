# Gen AI & Dataiku: LLM Mesh Use Cases

## Course Overview

Leverage Dataiku's LLM Mesh to build enterprise Gen AI applications. Learn to orchestrate multiple LLM providers, build RAG applications, and deploy production-grade AI solutions using Dataiku's visual and programmatic interfaces.

**Level:** Intermediate to Advanced
**Prerequisites:** Dataiku DSS basics, Python, LLM fundamentals
**Duration:** 5 modules (6-8 weeks)
**Effort:** 8-10 hours per week

## Why Dataiku for Gen AI?

Dataiku LLM Mesh provides:
- **Provider Abstraction**: Single API for multiple LLM providers
- **Governance**: Centralized cost tracking and access control
- **Integration**: Seamless connection to enterprise data
- **Visual Tools**: No-code RAG and prompt design
- **MLOps**: Full lifecycle management for Gen AI

## Learning Outcomes

By completing this course, you will:

1. **Configure** LLM Mesh connections to multiple providers
2. **Build** retrieval-augmented generation applications
3. **Design** effective prompts using Dataiku's Prompt Studios
4. **Deploy** LLM applications as APIs and web apps
5. **Monitor** Gen AI usage, costs, and performance
6. **Implement** guardrails and governance policies

## Course Structure

| Module | Topic | Key Skills |
|--------|-------|------------|
| 0 | LLM Mesh Foundations | Provider setup, connection config |
| 1 | Prompt Design | Prompt Studios, template variables |
| 2 | RAG Applications | Knowledge banks, vector stores |
| 3 | Custom Applications | Python recipes, custom models |
| 4 | Deployment & Governance | APIs, monitoring, cost management |

## Key Features Covered

### LLM Mesh

```
                    ┌─────────────────┐
                    │   LLM Mesh      │
                    │   (Dataiku)     │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
    ┌─────▼─────┐     ┌─────▼─────┐     ┌─────▼─────┐
    │  Claude   │     │   GPT-4   │     │  Azure    │
    │(Anthropic)│     │ (OpenAI)  │     │  OpenAI   │
    └───────────┘     └───────────┘     └───────────┘
```

### Knowledge Banks (RAG)

- Automatic chunking and embedding
- Vector store management
- Retrieval configuration
- Source attribution

### Prompt Studios

- Visual prompt design
- Variable injection
- Testing and iteration
- Version control

## Hands-On Labs

1. **Customer Support Bot**: RAG over documentation
2. **Report Summarizer**: Processing financial reports
3. **Data Quality Agent**: Automated data validation
4. **Code Assistant**: SQL and Python generation

## Technology Stack

**Dataiku DSS:**
- LLM Mesh connections
- Knowledge Banks
- Prompt Studios
- Webapps framework

**LLM Providers:**
- Anthropic Claude
- OpenAI GPT-4
- Azure OpenAI
- Google Vertex AI

## Setup Requirements

- Dataiku DSS 12.0+ with LLM Mesh license
- API keys for at least one LLM provider
- Administrator access for LLM Mesh configuration

---

*"Dataiku LLM Mesh brings Gen AI to enterprise data—governed, integrated, and production-ready."*
