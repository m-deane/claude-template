# Module 1: Report Processing

## Overview

Transform unstructured government and industry reports into structured, tradeable data. Learn to parse EIA petroleum reports, USDA crop forecasts, and earnings transcripts using LLMs.

**Time Estimate:** 8-10 hours

## Learning Objectives

By completing this module, you will:
1. Extract structured data from EIA Weekly Petroleum Status Reports
2. Parse USDA WASDE reports for grain supply/demand
3. Process earnings call transcripts for commodity mentions
4. Build robust extraction pipelines with validation

## Contents

### Guides
- `01_eia_reports.md` - Parsing EIA petroleum data
- `02_usda_reports.md` - WASDE and crop reports
- `03_earnings_transcripts.md` - Corporate commodity mentions

### Notebooks
- `01_eia_extraction.ipynb` - Automated EIA report parsing
- `02_usda_extraction.ipynb` - WASDE data extraction
- `03_transcript_analysis.ipynb` - Earnings call processing

## Key Concepts

### Extraction Pipeline

```
Raw Report (PDF/HTML)
        ↓
    Text Extraction
        ↓
    LLM Parsing (structured output)
        ↓
    Validation & Normalization
        ↓
    Structured Data (JSON/Database)
```

### Example: EIA Extraction

**Input (text):**
> "U.S. commercial crude oil inventories decreased by 5.2 million barrels
> from the previous week. At 430.0 million barrels, inventories are
> about 3% below the five year average for this time of year."

**Output (structured):**
```json
{
    "report_type": "weekly_petroleum_status",
    "metrics": [
        {
            "category": "crude_oil_inventory",
            "change": -5.2,
            "unit": "million_barrels",
            "total": 430.0,
            "vs_5yr_avg": -3,
            "vs_5yr_avg_unit": "percent"
        }
    ]
}
```

### Key Data Sources

| Source | Frequency | Commodities | Access |
|--------|-----------|-------------|--------|
| EIA WPSR | Weekly | Oil, Gas, Products | Free API |
| EIA STEO | Monthly | Energy forecasts | Free API |
| USDA WASDE | Monthly | Grains, Oilseeds | Free |
| IEA OMR | Monthly | Global Oil | Subscription |

## Prerequisites

- Module 0 completed
- Python with requests, beautifulsoup4
- Anthropic API access
