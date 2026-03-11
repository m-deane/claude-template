# Generate Tests

Generate comprehensive test suite for the specified file, component, or module.

## Current Testing Setup

- Detect the test framework by reviewing package.json, jest.config, vitest.config, or equivalent
- Review existing test files for patterns and conventions
- Check current test coverage if available
- Review the target file or component to understand what needs testing

## Task

Analyze the target code and create complete test coverage including:

1. Unit tests for individual functions and methods
2. Integration tests for component interactions
3. Edge case and error handling tests
4. Mock implementations for external dependencies
5. Test utilities and helpers as needed
6. Performance and snapshot tests where appropriate

## Process

Follow these steps:

1. Analyze the target file/component structure
2. Identify all testable functions, methods, and behaviors
3. Examine existing test patterns in the project
4. Create test files following project naming conventions
5. Implement comprehensive test cases with proper setup/teardown
6. Add necessary mocks and test utilities
7. Verify test coverage and add missing test cases

## Test Types

### Unit Tests

- Individual function testing with various inputs
- Component rendering and prop handling
- State management and lifecycle methods
- Utility function edge cases and error conditions

### Integration Tests

- Component interaction testing
- API integration with mocked responses
- Service layer integration
- End-to-end user workflows

### Framework-Specific Tests

- **React**: Component testing with React Testing Library
- **Vue**: Component testing with Vue Test Utils
- **Angular**: Component and service testing with TestBed
- **Node.js**: API endpoint and middleware testing

## Testing Best Practices

### Test Structure

- Use descriptive test names that explain the behavior
- Follow AAA pattern (Arrange, Act, Assert)
- Group related tests with describe blocks
- Use proper setup and teardown for test isolation

### Mock Strategy

- Mock external dependencies and API calls
- Use factories for test data generation
- Implement proper cleanup for async operations
- Mock timers and dates for deterministic tests

### Coverage Goals

- Aim for 80%+ code coverage
- Focus on critical business logic paths
- Test both happy path and error scenarios
- Include boundary value testing

Adapt to the project's testing framework (Jest, Vitest, Cypress, etc.) and follow established patterns.

Refer to @project-instructions for project-specific conventions.
