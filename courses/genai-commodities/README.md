# Generative AI for Commodities Trading & Fundamentals Analysis

## Course Overview

Apply generative AI and large language models to commodities markets—processing unstructured data, analyzing fundamental reports, building forecasting models, and automating trading research workflows.

**Level:** Advanced
**Prerequisites:** Commodities market knowledge, Python, ML fundamentals
**Duration:** 7 modules (10-12 weeks)
**Effort:** 10-12 hours per week

## Why Gen AI for Commodities?

Commodity markets are data-rich but information-poor. Key drivers are buried in:
- Government reports (EIA, USDA, IEA)
- Corporate filings and earnings calls
- News feeds and geopolitical developments
- Weather data and seasonal patterns

Gen AI excels at extracting, synthesizing, and reasoning over this unstructured information.

## Learning Outcomes

By completing this course, you will:

1. **Extract** structured data from commodity reports using LLMs
2. **Build** RAG systems for fundamental research
3. **Generate** trading signals from unstructured data
4. **Automate** research workflows with AI agents
5. **Combine** traditional quant models with LLM insights
6. **Deploy** AI-powered analysis pipelines

## Course Structure

| Module | Topic | Key Skills |
|--------|-------|------------|
| 0 | Foundations | Commodity markets, LLM basics |
| 1 | Report Processing | Parsing EIA, USDA, earnings calls |
| 2 | RAG for Research | Building commodity knowledge bases |
| 3 | Sentiment Analysis | News, social media, analyst reports |
| 4 | Fundamentals Modeling | Supply/demand, storage, term structure |
| 5 | Signal Generation | Converting analysis to trading signals |
| 6 | Production Systems | Pipelines, monitoring, deployment |

## Key Applications

### Report Extraction
```
Input: "U.S. crude oil production averaged 12.9 million b/d in 2023..."
Output: {commodity: "crude_oil", metric: "production", value: 12.9, unit: "million_bpd", year: 2023}
```

### Fundamental Analysis
```
Query: "What's the current supply/demand balance for natural gas?"
System: [Retrieves EIA storage report, weather forecasts, LNG export data]
Output: "Natural gas storage is 15% above 5-year average..."
```

### Trading Signals
```
Input: [EIA report, weather data, price action]
Output: {signal: "long", confidence: 0.72, rationale: "..."}
```

## Technology Stack

**LLM Providers:**
- Anthropic Claude (primary)
- OpenAI GPT-4 (alternative)

**Data Sources:**
- EIA API (energy data)
- USDA Reports (agriculture)
- IEA (international energy)
- NOAA (weather)

**Infrastructure:**
- LangChain/LangGraph
- ChromaDB/Pinecone
- pandas, numpy
- FastAPI for deployment

## Setup

```bash
pip install langchain langchain-anthropic chromadb
pip install pandas numpy matplotlib
pip install requests beautifulsoup4
pip install feedparser  # For news feeds
```

## API Keys Required

```bash
ANTHROPIC_API_KEY=your_key
EIA_API_KEY=your_eia_key  # Free from EIA
```

---

*"In commodities, information is perishable—the trader who extracts insights fastest has the edge. Gen AI is the extraction engine."*
