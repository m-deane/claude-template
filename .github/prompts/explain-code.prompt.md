---
mode: agent
description: "Explain complex code with detailed breakdown of logic, patterns, and flow"
tools: ["read", "search"]
---

# Explain Code

Provide detailed explanation of: ${input:target}

## Task

Analyze and explain the specified code with clarity and depth.

## Analysis Process

### 1. Overview
- **Purpose**: What does this code accomplish?
- **Context**: Where does it fit in the broader system?
- **Entry Points**: How is this code called/used?

### 2. Step-by-Step Breakdown

For each significant section:

```
Line X-Y: [Section Name]
-- What: [What this code does]
-- Why: [Why it's done this way]
-- How: [Technical implementation details]
-- Note: [Any gotchas or important considerations]
```

### 3. Data Flow

Trace the flow of data through the code:
- Inputs and their sources
- Transformations applied
- Outputs and their destinations
- Side effects (if any)

### 4. Control Flow

Map the execution path:
- Branching logic (if/else, switch)
- Loops and iterations
- Early returns and guards
- Exception handling

### 5. Design Patterns

Identify patterns used:
- **Creational**: Factory, Builder, Singleton
- **Structural**: Adapter, Decorator, Facade
- **Behavioral**: Strategy, Observer, Command
- **Architectural**: MVC, Repository, Service Layer

### 6. Dependencies

List and explain:
- External libraries/packages used
- Internal modules imported
- System resources accessed

### 7. Complexity Analysis

Assess:
- **Time Complexity**: Big O notation
- **Space Complexity**: Memory usage
- **Cognitive Complexity**: Readability/maintainability

### 8. Potential Issues

Flag any concerns:
- Edge cases not handled
- Performance bottlenecks
- Security considerations
- Error handling gaps
- Code smells

### 9. Related Code

Point to related components:
- Functions that call this code
- Functions this code calls
- Similar implementations elsewhere
- Tests for this code

## Explanation Levels

Adapt the explanation depth based on context:

- **Quick**: High-level overview, key points only
- **Standard**: Balanced explanation with important details
- **Deep**: Comprehensive analysis of every aspect
- **Beginner**: Extra context, no assumed knowledge
