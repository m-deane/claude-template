# Module 3: Memory & Context Management

## Overview

LLMs have no inherent memory—each API call starts fresh. This module teaches you to build memory systems that give agents persistent knowledge, from conversation history to semantic retrieval with RAG.

**Time Estimate:** 8-10 hours

## Learning Objectives

By completing this module, you will:
1. Implement conversation memory with context window management
2. Build RAG (Retrieval-Augmented Generation) pipelines
3. Design and query vector databases effectively
4. Combine multiple memory types for complex agents

## Contents

### Guides
- `01_conversation_memory.md` - Managing conversation history
- `02_rag_fundamentals.md` - Retrieval-Augmented Generation basics
- `03_vector_stores.md` - Embedding and storing knowledge

### Notebooks
- `01_memory_patterns.ipynb` - Implementing different memory types
- `02_rag_pipeline.ipynb` - Building a complete RAG system
- `03_advanced_retrieval.ipynb` - Hybrid search and reranking

## Key Concepts

### Memory Types

| Type | Persistence | Use Case |
|------|-------------|----------|
| Buffer | Session | Short conversations |
| Summary | Session | Long conversations |
| Vector | Permanent | Knowledge retrieval |
| Entity | Permanent | Tracking specific entities |
| Graph | Permanent | Relationship tracking |

### RAG Architecture

```
User Query
    ↓
Embed Query → Vector Search → Retrieve Documents
    ↓
Augment Prompt with Context
    ↓
LLM Generates Response with Citations
```

### Chunking Strategies

- **Fixed Size**: Split by character/token count
- **Semantic**: Split at natural boundaries
- **Recursive**: Hierarchical splitting
- **Document-Aware**: Respect structure (headers, paragraphs)

## Prerequisites

- Module 0-2 completed
- Understanding of embeddings (conceptual)
- Vector database access (Chroma, Pinecone, or similar)
