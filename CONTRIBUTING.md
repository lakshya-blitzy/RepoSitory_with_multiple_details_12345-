# Contributing to Testinium QA Python

Thank you for your interest in contributing to the Testinium QA Python test automation framework! We welcome contributions from the community and are grateful for your support in making this framework better.

This document provides comprehensive guidelines for contributing to the project. Whether you're fixing bugs, adding features, improving documentation, or helping with testing, your contributions are valued.

## Table of Contents

- [Getting Started as a Contributor](#getting-started-as-a-contributor)
- [Development Workflow](#development-workflow)
- [Code Style Guide](#code-style-guide)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Code of Conduct](#code-of-conduct)

## Getting Started as a Contributor

### Prerequisites

Before you begin contributing, ensure you have the following installed:

- **Python 3.9 or higher** (Python 3.12 recommended)
- **Git** for version control
- **pip** (Python package manager)
- **Virtual environment tool** (`venv` or `virtualenv`)

### Development Environment Setup

1. **Fork the Repository**

   Fork the repository on GitHub by clicking the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/Testinium-QA.git
   cd Testinium-QA
   ```

3. **Add Upstream Remote**

   ```bash
   git remote add upstream https://github.com/BalamiRR/Testinium-QA.git
   ```

4. **Create Virtual Environment**

   **On macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **On Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Install Dependencies**

   ```bash
   # Install runtime dependencies
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install pylint black mypy isort pytest-cov
   ```

6. **Verify Installation**

   ```bash
   # Run existing tests to ensure setup is correct
   behave --dry-run
   pytest tests/
   ```

### IDE Configuration

**PyCharm:**
- Enable Black formatter: `Settings > Tools > Black`
- Configure line length to 100: `Settings > Editor > Code Style > Python > Line length: 100`
- Enable type checking with mypy: `Settings > Tools > Python Integrated Tools`

**Visual Studio Code:**
- Install Python extension
- Install Gherkin syntax highlighting extension
- Configure Black as formatter in `.vscode/settings.json`:
  ```json
  {
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "editor.formatOnSave": true
  }
  ```

### Pre-commit Hooks (Recommended)

Install pre-commit hooks to automatically check code quality before commits:

```bash
pip install pre-commit
pre-commit install
```

This will run Black, isort, and pylint automatically before each commit.

## Development Workflow

### Branch Naming Conventions

Create descriptive branch names following these patterns:

- **Feature branches:** `feature/add-new-wait-helper`
- **Bug fix branches:** `fix/stale-element-handling`
- **Documentation branches:** `docs/update-api-reference`
- **Refactoring branches:** `refactor/improve-driver-manager`
- **Test branches:** `test/add-config-tests`

### Creating a Feature Branch

```bash
# Ensure you're on the main branch and up to date
git checkout main
git pull upstream main

# Create and switch to a new feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. **Make your changes** in the appropriate files
2. **Write or update tests** for your changes
3. **Update documentation** if needed (docstrings, README.md, or docs/)
4. **Run tests locally** to ensure everything works
5. **Run code quality checks** (see below)

### Commit Message Standards

Write clear, descriptive commit messages following these guidelines:

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
git commit -m "feat(pages): add InventoryPage with product search functionality"
git commit -m "fix(driver_manager): resolve thread-safety issue in driver initialization"
git commit -m "docs(api): update wait_helpers documentation with new examples"
git commit -m "test(config): add unit tests for environment variable precedence"
```

### Keeping Your Fork Updated

Regularly sync your fork with the upstream repository:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Code Style Guide

We follow strict code quality standards to ensure consistency and maintainability across the codebase.

### PEP 8 Compliance

All Python code must comply with [PEP 8](https://pep8.org/) style guide with the following specifications:

- **Line length:** Maximum 100 characters (not the default 79)
- **Indentation:** 4 spaces (no tabs)
- **Naming conventions:**
  - Classes: `PascalCase` (e.g., `LoginPage`, `DriverManager`)
  - Functions/methods: `snake_case` (e.g., `get_driver`, `wait_for_element`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TIMEOUT`, `DEFAULT_BROWSER`)
  - Private methods: prefix with underscore `_private_method`

### Black Formatting

All code must be formatted with [Black](https://github.com/psf/black):

```bash
# Format all Python files
black --line-length 100 .

# Check formatting without making changes
black --check --line-length 100 .
```

**Configuration:** Black settings are in `pyproject.toml`:
```toml
[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311', 'py312']
```

### Import Sorting with isort

Organize imports using [isort](https://pycqa.github.io/isort/):

```bash
# Sort imports in all files
isort .

# Check import sorting
isort --check-only .
```

**Import Order:**
1. Standard library imports
2. Third-party imports (selenium, behave, pytest, etc.)
3. Local application imports

**Example:**
```python
import os
import sys
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import behave

from config.test_config import get_config
from utilities.driver_manager import DriverManager
```

### Type Hints

Use type hints for all function signatures (Python 3.9+ syntax):

```python
from typing import Optional, List, Dict, Any
from selenium.webdriver.remote.webelement import WebElement

def wait_for_element(
    self,
    locator: tuple[By, str],
    timeout: Optional[int] = None
) -> WebElement:
    """Wait for element to be present and return it."""
    pass

def get_all_elements(self, locator: tuple[By, str]) -> List[WebElement]:
    """Get all elements matching the locator."""
    pass
```

**Check type hints with mypy:**
```bash
mypy config/ utilities/ pages/ features/
```

### Docstring Standards

Follow [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) as per PEP 257:

**Module-level docstring:**
```python
"""Module for managing WebDriver instances with thread-safety.

This module provides the DriverManager class which handles WebDriver
lifecycle management with thread-local storage for parallel execution.

Example:
    from utilities.driver_manager import DriverManager
    
    driver = DriverManager.get_driver()
    driver.get("https://example.com")
    DriverManager.quit_driver()
"""
```

**Class docstring:**
```python
class LoginPage(BasePage):
    """Page Object Model for the login page.
    
    Provides methods and properties for interacting with login page elements
    including email input, password input, and login button.
    
    Attributes:
        _INPUT_EMAIL: Locator for email input field
        _INPUT_PASSWORD: Locator for password input field
        _LOGIN_BUTTON: Locator for login submit button
    """
```

**Method docstring:**
```python
def wait_for_clickable(
    self,
    locator: tuple[By, str],
    timeout: Optional[int] = None
) -> WebElement:
    """Wait for element to be clickable and return it.
    
    Waits for element to be both visible and enabled, ready for interaction.
    Uses explicit wait with configurable timeout.
    
    Args:
        locator: Tuple of (By strategy, locator string)
        timeout: Maximum wait time in seconds. Uses config default if None.
        
    Returns:
        WebElement that is clickable
        
    Raises:
        TimeoutException: If element not clickable within timeout period
        
    Example:
        >>> login_button = page.wait_for_clickable((By.ID, "login-btn"))
        >>> login_button.click()
    """
```

### Code Quality Checks

Run these checks before committing:

```bash
# Format code
black --line-length 100 .

# Sort imports
isort .

# Lint code
pylint config/ utilities/ pages/ features/

# Type check
mypy config/ utilities/ pages/ features/

# Run all checks together
black --check . && isort --check-only . && pylint config/ utilities/ pages/ features/ && mypy .
```

## Testing Guidelines

### Writing Tests

**Every new feature must include tests.** We use both Behave for BDD tests and pytest for unit tests.

### Unit Test Structure

Place unit tests in the `tests/` directory:

```
tests/
├── __init__.py
├── test_config.py
├── test_driver_manager.py
├── test_wait_helpers.py
└── test_page_objects.py
```

**Example unit test:**
```python
import pytest
from unittest.mock import Mock, patch
from utilities.driver_manager import DriverManager

class TestDriverManager:
    """Test suite for DriverManager class."""
    
    def test_get_driver_returns_webdriver_instance(self):
        """Test that get_driver returns a WebDriver instance."""
        driver = DriverManager.get_driver()
        assert driver is not None
        DriverManager.quit_driver()
    
    @patch('utilities.driver_manager.webdriver.Chrome')
    def test_get_driver_creates_chrome_driver(self, mock_chrome):
        """Test Chrome driver creation with mocked WebDriver."""
        mock_instance = Mock()
        mock_chrome.return_value = mock_instance
        
        driver = DriverManager.get_driver()
        
        assert mock_chrome.called
        assert driver == mock_instance
```

### Mocking Strategies for WebDriver

When writing unit tests, mock WebDriver to avoid browser launches:

```python
from unittest.mock import Mock, patch, MagicMock

# Mock WebDriver
@patch('selenium.webdriver.Chrome')
def test_page_object_interaction(mock_chrome):
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    
    # Mock WebElement
    mock_element = Mock()
    mock_driver.find_element.return_value = mock_element
    
    # Test your page object
    page = LoginPage(mock_driver)
    element = page.input_email
    
    assert element == mock_element
```

### Running Tests

```bash
# Run all Behave tests
behave

# Run specific feature
behave features/Login.feature

# Run with specific tags
behave --tags=@Login

# Run pytest unit tests
pytest tests/

# Run with coverage report
pytest --cov=config --cov=utilities --cov=pages --cov-report=html tests/

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

### Coverage Requirements

- **Minimum coverage:** 80% for all new code
- **Target coverage:** 90%+ for critical modules (driver_manager, config_reader, wait_helpers)
- **Check coverage:** `pytest --cov=. --cov-report=term-missing tests/`

All pull requests must maintain or improve overall test coverage.

### Test Best Practices

1. **Test one thing per test method**
2. **Use descriptive test names** that explain what is being tested
3. **Follow AAA pattern:** Arrange, Act, Assert
4. **Clean up resources** in teardown methods
5. **Mock external dependencies** (WebDriver, file system, network)
6. **Test edge cases and error conditions**
7. **Keep tests fast** (< 1 second per unit test)

## Documentation Standards

Good documentation is as important as good code. Update documentation whenever you make changes.

### When to Update Documentation

Update documentation in these scenarios:

1. **Adding new features:** Document public APIs, add user guide examples
2. **Changing APIs:** Update API reference and affected guides
3. **Fixing bugs:** Update troubleshooting guide if it's a common issue
4. **Changing configuration:** Update configuration reference documentation
5. **Adding dependencies:** Update dependencies documentation

### Docstring Updates

- **Always update docstrings** when modifying functions or classes
- **Include examples** for complex methods
- **Document parameters and return values** with types
- **Document exceptions** that can be raised

### Markdown Documentation

For documentation in `docs/` directory:

**Formatting standards:**
- Use ATX-style headers (`# ## ###`)
- Include code blocks with language identifiers
- Use tables for structured data
- Add links to related documentation

**Example:**
```markdown
## Using Wait Helpers

The `WaitHelpers` class provides explicit wait utilities:

```python
from utilities.wait_helpers import WaitHelpers

# Wait for element to be visible
element = wait_helpers.wait_for_visibility(locator, timeout=10)
```

See also:
- [API Reference: WaitHelpers](../api-reference/utilities/wait-helpers.md)
- [Architecture: Wait Strategies](../architecture/wait-strategies.md)
```

### Code Examples in Documentation

All code examples must be:
- **Syntactically correct** and tested
- **Complete** with necessary imports
- **Realistic** with meaningful variable names
- **Concise** (under 20 lines when possible)

## Pull Request Process

### Before Submitting a Pull Request

Complete this checklist:

- [ ] Code follows PEP 8 and project style guidelines
- [ ] Code is formatted with Black (line length 100)
- [ ] Imports are sorted with isort
- [ ] Type hints are added to all function signatures
- [ ] Docstrings are added/updated for all public APIs
- [ ] Unit tests are written for new functionality
- [ ] All tests pass locally (`behave` and `pytest tests/`)
- [ ] Code coverage is maintained or improved
- [ ] Documentation is updated (docstrings, README.md, docs/)
- [ ] Commit messages follow the standard format
- [ ] Branch is up to date with upstream main

### Creating a Pull Request

1. **Push your branch to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub from your branch to `upstream/main`

3. **Fill out the PR template** with:
   - Clear description of changes
   - Related issue numbers (if applicable)
   - Testing performed
   - Screenshots (if UI-related)

4. **Request review** from maintainers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Other (specify)

## Related Issues
Closes #123

## Testing Performed
- [ ] All existing tests pass
- [ ] New tests added for this change
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
```

### Review Criteria

Pull requests will be reviewed based on:

1. **Code Quality:**
   - Follows project style guidelines
   - Well-structured and maintainable
   - No code smells or anti-patterns
   - Appropriate use of design patterns

2. **Testing:**
   - Adequate test coverage (minimum 80%)
   - Tests are meaningful and comprehensive
   - Edge cases are covered
   - Tests pass consistently

3. **Documentation:**
   - Docstrings are complete and accurate
   - User-facing documentation is updated
   - API changes are documented
   - Examples are provided where appropriate

4. **Functionality:**
   - Code works as intended
   - No regressions introduced
   - Performance is acceptable
   - Thread-safety considered (where applicable)

### CI Requirements

All pull requests must pass Continuous Integration checks:

- **Linting:** pylint with score >= 8.0
- **Formatting:** Black and isort checks pass
- **Type Checking:** mypy passes with no errors
- **Tests:** All Behave and pytest tests pass
- **Coverage:** Test coverage >= 80%

**CI pipeline runs automatically** on every pull request. Fix any failures before requesting review.

### Merge Process

1. **Approval:** At least one maintainer approval required
2. **CI Checks:** All CI checks must pass
3. **Conflicts:** Resolve any merge conflicts
4. **Merge:** Maintainer will merge using "Squash and Merge"

## Issue Reporting

### Reporting Bugs

Found a bug? Please report it!

**Before creating an issue:**
1. Check if the issue already exists
2. Verify it's not listed in the troubleshooting guide
3. Ensure you're using the latest version

**Create a bug report** using our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)

**Include:**
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, browser)
- Error messages and stack traces
- Screenshots (if applicable)

### Requesting Features

Have an idea for a new feature?

**Create a feature request** using our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)

**Include:**
- Clear description of the feature
- Use case and benefits
- Proposed implementation approach
- Alternatives considered

### Asking Questions

For questions about usage:
- Check the documentation first
- Search existing issues
- Ask in GitHub Discussions (if enabled)
- Open an issue with the "question" label

## Code of Conduct

### Our Standards

We are committed to providing a welcoming and inclusive environment. We expect all contributors to:

- **Be respectful** and considerate in communication
- **Be collaborative** and constructive in feedback
- **Be patient** with new contributors
- **Accept constructive criticism** gracefully
- **Focus on what's best** for the community and project

### Unacceptable Behavior

The following behaviors are unacceptable:

- Harassment, discrimination, or offensive comments
- Personal attacks or insults
- Trolling or inflammatory comments
- Publishing others' private information
- Any conduct that could reasonably be considered inappropriate

### Enforcement

Project maintainers are responsible for enforcing these standards. Unacceptable behavior may result in:

1. Warning from maintainers
2. Temporary ban from the project
3. Permanent ban from the project

### Reporting Issues

If you experience or witness unacceptable behavior, please contact the project maintainers privately via email or GitHub.

## Recognition

### Contributors

We recognize all types of contributions:

- **Code contributions:** Features, bug fixes, refactoring
- **Documentation:** Writing or improving documentation
- **Testing:** Writing tests, reporting bugs
- **Support:** Helping others in issues and discussions
- **Ideas:** Feature requests and suggestions

All contributors will be acknowledged in our README and release notes.

### Becoming a Maintainer

Active contributors who demonstrate:
- Deep understanding of the codebase
- Consistent high-quality contributions
- Helpful engagement with the community
- Alignment with project values

may be invited to become maintainers with commit access.

## Getting Help

Need help contributing?

- **Documentation:** Check our [comprehensive docs](docs/)
- **Examples:** See existing code for patterns
- **Questions:** Open an issue with the "question" label
- **Community:** Engage in GitHub Discussions

## Thank You!

Thank you for contributing to Testinium QA Python! Your efforts help make this framework better for everyone.

**Happy coding! :leaves:**

---

**Source:** README.md Contributing section (lines 740-750), expanded per Agent Action Plan 0.5 requirements

