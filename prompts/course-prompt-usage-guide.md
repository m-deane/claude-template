# Fair Value Commodities Course - Prompt Usage Guide

## Quick Start

The main prompt file `fair-value-commodities-course-prompt.md` contains a complete, self-contained instruction set for generating a 40-hour course on "Fair Value Modelling in Commodities Trading: From Point-in-Time Data to Signal Discovery".

### To Use This Prompt:

1. **Direct Generation**: Copy the entire prompt and provide it to an AI system (Claude, GPT-4, etc.) to generate the complete course materials
2. **Module-by-Module**: For better quality, generate one module at a time by extracting the relevant module specification
3. **Component Generation**: Use sections of the prompt to generate specific components (e.g., just the code examples, just the quizzes)

## Key Differentiators This Prompt Emphasizes

### 1. Temporal Data Discipline
Unlike generic courses that treat data as static, this course makes point-in-time data management central to EVERY module:
- Data has both observation dates (when events occurred) and publication dates (when we learned about them)
- All code respects what was knowable at each point in time
- Backtesting simulates real trading constraints
- Data revisions are tracked and analyzed

### 2. Fair Value as Fundamental Equilibrium
The course defines fair value through physical market dynamics, NOT technical analysis:
- Supply-demand balance models
- Inventory-to-consumption ratios
- Cost curve analysis
- Seasonal adjustments based on fundamentals
- Production economics and marginal costs

### 3. Signal Discovery Focus
Rather than just predicting prices, the course emphasizes finding tradeable divergences:
- When market prices deviate from fundamental fair value
- Statistical significance of divergences
- Regime-dependent signal reliability
- Position sizing based on convergence probability
- Entry/exit timing optimization

### 4. Production-Ready Implementation
Every module includes real, working code that could be deployed:
```python
# Example from the prompt showing actual implementation structure
class PointInTimeRecord:
    series_id: str              # e.g., "EIA.CRUDE.STOCKS"
    observation_date: datetime  # Date data refers to
    publication_date: datetime  # When data was released
    as_of_date: datetime       # When we knew this value
    value: float               # The actual data point
```

## Module Breakdown

### Foundation Modules (1-4): Data & Concepts
- **Module 1**: Commodities fair value fundamentals
- **Module 2**: Point-in-time data architecture
- **Module 3**: Temporal-aware exploratory data analysis
- **Module 4**: Fundamental data sources with proper timestamps

### Core Modeling (5-7): Building Fair Value Models
- **Module 5**: Fair value model construction (inventory, cost curve, ML)
- **Module 6**: Feature engineering with temporal constraints
- **Module 7**: Walk-forward validation and backtesting

### Trading Application (8-10): From Model to P&L
- **Module 8**: Signal discovery and trading logic
- **Module 9**: Production systems and real-time trading
- **Module 10**: Advanced topics and case studies

## Expected Outputs

When you use this prompt, the AI should generate:

### Per Module (4 hours of content each):
- 3000-4000 words of conceptual explanation
- 10+ complete Python code examples (runnable, not pseudo-code)
- Mathematical formulations where relevant
- 3-4 hands-on exercises with solutions
- 10-15 quiz questions with answers
- Real data examples or instructions to obtain data
- Common pitfalls and debugging guides

### Complete Course Package:
- 40 hours of instructional content
- Comprehensive codebase with `fair_value_toolkit` library
- Sample datasets and data fetching scripts
- Assessment materials and grading rubrics
- Capstone project specifications

## Quality Checklist

The generated course should meet these criteria:

☐ **Temporal Integrity**: Every example shows observation vs publication dates
☐ **No Look-Ahead Bias**: All backtests properly simulate point-in-time constraints
☐ **Fundamental Focus**: Fair value from supply/demand, not technical indicators
☐ **Signal Emphasis**: Finding divergences, not just forecasting
☐ **Revision Handling**: Data revisions analyzed in every module
☐ **Trading Reality**: Transaction costs, market impact, regime changes
☐ **Production Ready**: Code that could actually be deployed
☐ **Progressive Building**: Each module builds on previous concepts

## Common Issues and Solutions

### If Output is Too Generic:
- Emphasize the temporal/vintage aspects more strongly
- Point to specific sections about point-in-time data
- Request concrete code examples, not descriptions

### If Missing Trading Focus:
- Highlight Module 8 specifications on signal generation
- Emphasize divergence detection over price prediction
- Request P&L attribution examples

### If Code is Incomplete:
- Specify "complete, runnable Python code"
- Request full class implementations
- Ask for error handling and edge cases

## Example Usage Patterns

### Generate Single Module:
"Using the specifications for Module 2: Point-in-Time Data Architecture from this prompt, generate the complete module content including all code examples, exercises, and assessment materials."

### Generate Code Library:
"Based on this course specification, implement the complete `fair_value_toolkit` Python library with all classes and functions mentioned in the code examples."

### Generate Data Examples:
"Create sample datasets for Module 5 that demonstrate real revision patterns in EIA crude oil inventory data, including proper observation and publication timestamps."

## Extensions and Customizations

The prompt can be modified for:
- Different commodities focus (energy, agriculture, metals)
- Different programming languages (R, Julia, C++)
- Different market regions (European power, Asian metals)
- Different skill levels (beginner, advanced)
- Shorter/longer course durations

## Contact and Support

This prompt was designed to create a course that addresses real gaps in commodities trading education:
1. Most courses ignore temporal data issues
2. Few teach practical signal discovery
3. Revision handling is rarely covered
4. Production implementation is often missing

The result should be a course that could genuinely prepare someone to build and trade fair value models in commodity markets with proper risk controls and realistic expectations.