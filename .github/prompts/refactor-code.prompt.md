---
mode: agent
description: "Intelligently refactor and improve code quality"
tools: ["read", "edit", "execute", "search"]
---

# Intelligently Refactor and Improve Code Quality

## Instructions

Follow this systematic approach to refactor code: **${input:target}**

1. **Pre-Refactoring Analysis**
   - Identify the code that needs refactoring and the reasons why
   - Understand the current functionality and behavior completely
   - Review existing tests and documentation
   - Identify all dependencies and usage points

2. **Test Coverage Verification**
   - Ensure comprehensive test coverage exists for the code being refactored
   - If tests are missing, write them BEFORE starting refactoring
   - Run all tests to establish a baseline
   - Document current behavior with additional tests if needed

3. **Refactoring Strategy**
   - Define clear goals for the refactoring (performance, readability, maintainability)
   - Choose appropriate refactoring techniques:
     - Extract Method/Function
     - Extract Class/Component
     - Rename Variable/Method
     - Move Method/Field
     - Replace Conditional with Polymorphism
     - Eliminate Dead Code
   - Plan the refactoring in small, incremental steps

4. **Incremental Refactoring**
   - Make small, focused changes one at a time
   - Run tests after each change to ensure nothing breaks
   - Commit working changes frequently with descriptive messages

5. **Code Quality Improvements**
   - Improve naming conventions for clarity
   - Eliminate code duplication (DRY principle)
   - Simplify complex conditional logic
   - Reduce method/function length and complexity
   - Improve separation of concerns

6. **Design Pattern Application**
   - Apply appropriate design patterns where beneficial
   - Improve abstraction and encapsulation
   - Enhance modularity and reusability
   - Reduce coupling between components

7. **Error Handling Improvement**
   - Standardize error handling approaches
   - Improve error messages and logging
   - Add proper exception handling
   - Enhance resilience and fault tolerance

8. **Documentation Updates**
   - Update code comments to reflect changes
   - Revise API documentation if interfaces changed
   - Update inline documentation and examples

9. **Integration Testing**
   - Run full test suite to ensure no regressions
   - Test integration with dependent systems
   - Verify all functionality works as expected
   - Test edge cases and error scenarios

10. **Documentation of Changes**
    - Create a summary of refactoring changes
    - Document any breaking changes or new patterns
    - Explain benefits and reasoning for future reference

Remember: Refactoring should preserve external behavior while improving internal structure. Always prioritize safety over speed, and maintain comprehensive test coverage throughout the process.
