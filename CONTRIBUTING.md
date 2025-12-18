# Contributing to Sweetviz

We welcome contributions in the form of bug reports, feature requests, and pull requests (PRs). This document describes how you can contribute.

## Bug Reports and Feature Requests

Please submit bug reports and feature requests as GitHub issues. This helps us to keep track of them and discuss potential solutions or enhancements.

## Pull Requests

We appreciate your pull requests. For small changes, feel free to submit a PR directly. If you are considering a large or significant change, please discuss it in a GitHub issue before submitting the PR. This will save both you and the maintainers time, and it helps to ensure that your contributions can be integrated smoothly.

## Writing Tests

Sweetviz follows a test-driven contribution model inspired by projects like aider. When contributing fixes or features:

### For Bug Fixes:

1. **First, write a test that demonstrates the bug** - Create a test that fails because of the bug you're fixing.
2. **Implement the fix** - Write code that addresses the issue.
3. **Verify the test passes** - Ensure your fix makes the test pass.

### For New Features:

1. **Write tests for the expected behavior** - Define what success looks like.
2. **Implement the feature** - Write the code.
3. **Ensure all tests pass** - Verify your implementation works correctly.

### Test Structure

Our test suite is organized as follows:

- `tests/unit/` - Unit tests for individual modules and functions
- `tests/integration/` - Integration tests for end-to-end functionality
- `tests/fixtures/` - Test fixtures and helper functions
- `tests/data/` - Test data files (when needed)

### Running Tests

We use `uv` for dependency management and running tests:

```bash
# Sync test dependencies (installs sweetviz and test tools)
uv sync --extra test --no-dev

# Run all tests with coverage and parallel execution
uv run pytest --cov=sweetviz -n auto

# Run only unit tests
uv run pytest tests/unit/ -n auto

# Run only integration tests  
uv run pytest tests/integration/ -n auto

# Run tests with detailed coverage report
uv run pytest --cov=sweetviz --cov-report=term --cov-report=html -n auto

# Skip slow tests
uv run pytest -m "not slow" -n auto
```

### Writing Good Tests

- **Be specific**: Test one behavior per test function
- **Use descriptive names**: `test_analyze_with_empty_dataframe` not `test_analyze_1`
- **Test edge cases**: Empty data, NaN values, single values, large datasets
- **Use fixtures**: For common test data setup
- **Property-based tests**: Use hypothesis for testing invariants with random data

### Example Test Pattern

```python
def test_feature_with_edge_case():
    """Test that feature handles edge case correctly."""
    # Arrange: Setup test data
    df = pd.DataFrame({'col': []})

    # Act: Call the function
    result = sweetviz.analyze(df)

    # Assert: Verify expected behavior
    assert result is not None
    html = result.show_html()
    assert isinstance(html, str)
    assert len(html) > 0
```

## Setting up a Development Environment

### Clone the Repository

```bash
git clone https://github.com/fbdesignpro/sweetviz.git
cd sweetviz
```

### Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install in Development Mode

```bash
uv sync --extra dev --extra test
```

This installs sweetviz and all development dependencies (including test tools, ruff, and pyrefly).

## Code Quality

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality. Install them with:

```bash
pip install pre-commit
pre-commit install
```

The hooks will run automatically on `git commit` and check:
- Code formatting and import sorting with ruff
- Linting with ruff
- Type checking with pyrefly

### Code Style

- Follow PEP 8
- Maximum line length: 88 characters
- Use type hints where appropriate
- Document public functions with docstrings

## Continuous Integration

All pull requests run through GitHub Actions CI which:

- Runs tests on Linux, macOS, and Windows
- Tests Python 3.10 through 3.13
- Reports test coverage
- Checks code formatting with ruff

Ensure all CI checks pass before requesting review.

## License

By contributing to Sweetviz, you agree that your contributions will be licensed under the project's MIT License.
