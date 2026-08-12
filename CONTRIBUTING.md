# Contributing to Core Automation Framework

Thank you for contributing to the Core Automation Framework! This document provides guidelines for contributing code, tests, and documentation.

# Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Writing Tests](#writing-tests)
- [Code Style & Standards](#code-style--standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Review Process](#review-process)


# Code of Conduct

All contributors are expected to:
- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards other members
- Report concerns to project maintainers

### 1. Fork and Clone Repository

powershell
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Core_Automation.git
cd Core_Automation

# Add upstream remote to track original repository
git remote add upstream https://github.com/ORIGINAL_OWNER/Core_Automation.git


### 2. Create Feature Branch

Always create a new branch for your contribution:

powershell
# Update main branch
git fetch upstream
git checkout main
git rebase upstream/main

# Create feature branch with descriptive name
git checkout -b feature/add-new-module
# or
git checkout -b fix/fix-flaky-test
# or
git checkout -b docs/update-readme
```

### 3. Set Up Development Environment

powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
playwright install

# Development Workflow

# Making Changes

1. *Write your code* following the [Code Style](#code-style--standards) guidelines
2. *Test thoroughly* with your changes
3. *Update documentation* if you changed functionality
4. *Run the test suite* to ensure nothing broke

# Running Tests Locally

powershell
# Run all tests
pytest

# Run specific module tests
pytest -m module_ap -v

# Run with coverage
pytest --cov=modules tests/

# Run in parallel
pytest -n auto

# Run specific file
pytest tests/home/test_home.py -v

# Linting & Code Quality

powershell
# Install linting tools (optional but recommended)
pip install flake8 black pylint

# Check code style
flake8 modules/ utils/

# Auto-format code
black modules/ utils/

# Check imports
pylint modules/ utils/

# Writing Tests

# Test Structure

Follow this structure for new tests:

python
import pytest
from modules.my_module.pages.my_page import MyPage

@pytest.mark.smoke  # or @pytest.mark.regression
@pytest.mark.module_name  # Add appropriate module marker
class TestMyFeature:
    """Test suite for My Feature"""
    
    def test_feature_should_work(self, authenticated_page):
        """
        Verify feature works as expected
        
        GIVEN: Precondition
        WHEN: Action is performed
        THEN: Expected result occurs
        """
        # Arrange
        page = MyPage(authenticated_page)
        
        # Act
        result = page.perform_action()
        
        # Assert
        assert result == expected_value, "Descriptive assertion message"
```

# Test Naming Convention

- Test files: `test_*.py`
- Test functions: `test_<action>_<expected_result>`
- Test classes: `Test<FeatureName>`

Examples:
python
def test_user_can_login():
def test_search_returns_matching_projects():
def test_create_ap_with_valid_data():
def test_error_message_shown_on_invalid_input():


# Adding New Test Markers

Edit "pytest.ini" and add your marker:

ini
markers =
    smoke: small set of critical tests
    regression: full regression suite
    module_ap: Analytic Plan Module tests
    my_new_marker: Description of your marker

---

# Code Style & Standards

# Python Style Guide (PEP 8)

  python
#  Good
def validate_project_name(project_name: str) -> bool:
    """Validate that project name is not empty."""
    if not project_name or not isinstance(project_name, str):
        return False
    return len(project_name.strip()) > 0


#  Bad
def validate_project_name(project_name):
    if project_name:
        return len(project_name) > 0
    else:
        return False


# Type Hints

Always add type hints:

   python
#  Good
from typing import Optional, List

def search_projects(query: str, limit: int = 10) -> List[str]:
    """Search for projects by name."""
    pass

def get_preference(key: str) -> Optional[str]:
    """Get user preference or None if not set."""
    pass


#  Bad
def search_projects(query, limit=10):
    pass


### Docstrings

Use Google-style docstrings:

   python
#  Good
def create_analytical_plan(self, databases: dict) -> bool:
    """Create a new analytical plan with specified databases.
    
    Args:
        databases: Dictionary with 'primary' and 'secondary' keys
        
    Returns:
        True if plan created successfully, False otherwise
        
    Raises:
        TimeoutError: If page elements not found within timeout
        ValueError: If databases dictionary is invalid
        
    Example:
        >>> ap_page = AnalyticalPlanPage(page)
        >>> result = ap_page.create_analytical_plan({
        ...     'primary': 'DB1',
        ...     'secondary': 'DB2'
        ... })
        >>> assert result is True
    """
    pass


#  Bad
def create_analytical_plan(self, databases):
    # Create AP
    pass
```

# Logging

Use appropriate log levels:

   python
import logging

logger = logging.getLogger(__name__)

logger.debug("Detailed info for debugging")      # Low-level details
logger.info("Test started")                      # General information
logger.warning("Element took 10s to load")       # Warning condition
logger.error("Failed to find element")           # Error occurred
logger.critical("Cannot login - no auth state")  # Critical failure
```

# Page Object Best Practices

   python
#  Good
class MyPage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(__name__)
    
    def click_submit_button(self) -> None:
        """Click the submit button and wait for processing."""
        try:
            button = self.page.get_by_role("button", name="Submit")
            button.wait_for(state="visible", timeout=5000)
            button.click()
            self.logger.info("Clicked submit button")
        except TimeoutError as e:
            self.logger.error(f"Submit button not found: {e}")
            raise


#  Bad
class MyPage:
    def __init__(self, page):
        self.page = page
    
    def submit(self):
        self.page.locator(".submit-btn").click()  # Hard to maintain


# File Organization


modules/
├── my_module/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── my_page.py              # 150-300 lines max
│   │   └── my_page_locator.py      # Locators only
│   └── __init__.py

tests/
├── my_module/
│   ├── __init__.py
│   ├── test_feature_a.py           # One logical feature per file
│   └── test_feature_b.py

---

# Commit Message Guidelines

Use clear, descriptive commit messages:

# Format

<type>(<scope>): <subject>

<body>

<footer>


# Type
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **test**: Test additions/modifications
- **refactor**: Code refactoring without features/fixes
- **perf**: Performance improvements
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **ci**: CI/CD configuration changes

# Scope
- **modules**: Changes to page objects
- **tests**: Changes to test files
- **utils**: Changes to utility functions
- **config**: Changes to configuration
- **ci**: Changes to CI/CD

# Examples

   bash
# Feature
git commit -m "feat(modules): add analytical plan locators"

# Bug fix
git commit -m "fix(tests): handle dynamic wait for dropdown elements"

# Documentation
git commit -m "docs(readme): update installation instructions"

# Test addition
git commit -m "test(modules): add tests for project search"

# Multiple changes
git commit -m "refactor(utils): consolidate wait helper methods

- Extract common wait logic into base_page
- Improve error messages
- Add type hints for all locator methods

# Submitting Pull Requests

# Before Submitting

1. **Sync with upstream**:
   powershell
   git fetch upstream
   git rebase upstream/main
   

2. **Run full test suite**:
   powershell
   pytest
   pytest -m smoke -v
   

3. **Verify your code style**:
   powershell
   flake8 modules/ utils/
   black --check modules/ utils/
   

4. **Update documentation**:
   - Add docstrings to new functions
   - Update README.md if needed
   - Update SETUP_GUIDE.md if setup changed

5. **Keep commits clean**:
      powershell
   # Squash multiple commits if needed
   git rebase -i upstream/main
   

### Creating Pull Request

1. **Push to your fork**:
   powershell
   git push origin feature/my-feature
   

2. **Create PR on GitHub**:
   - Title: Clear description of changes
   - Description: Use PR template (if available)
   - Link related issues: "Closes #123"

# PR Title Template

[TYPE] Brief description of changes

feat: Add analytical plan module
fix: Resolve timeout issues in base page
docs: Update contributing guidelines
test: Add comprehensive test suite for home page

# PR Description Template

   markdown
# Description
Brief explanation of what this PR does

# Changes Made
- Change 1
- Change 2
- Change 3

# Testing
- How was this tested?
- What test cases were added/modified?
- Any edge cases handled?

# Screenshots (if UI changes)
[Add screenshots if applicable]

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing locally
- [ ] Commits are descriptive
---

## Review Process

# What We Look For

1. **Code Quality**:
   - Follows PEP 8 style guide
   - Has proper type hints
   - Includes docstrings
   - No code duplication

2. **Testing**:
   - New tests added for new functionality
   - Existing tests still pass
   - Good test coverage
   - Tests are maintainable

3. **Documentation**:
   - Comments explain "why", not "what"
   - Docstrings are present
   - README updated if needed
   - Examples provided for new features

4. **Performance**:
   - No unnecessary waits
   - Efficient selectors
   - Minimal page reloads

# Review Timeline

- GitHub maintainers will review within 2-3 business days
- We may request changes
- Once approved, PR will be merged to main branch
- Changes will appear in next release

# Common Contribution Types

# Adding a New Test Module

1. Create folder structure:
   
   modules/my_module/pages/
   ├── __init__.py
   ├── my_module.py          # Page object
   └── my_module_locator.py  # Locators
   
   tests/my_module/
   ├── __init__.py
   └── test_my_module.py
   

2. Implement page object:
      python
   from modules.my_module.pages.my_module_locator import MyModuleLocator
   
   class MyModulePage:
       def __init__(self, page: Page):
           self.page = page
           self.locator = MyModuleLocator(page)
   

3. Add locators:
      python
   class MyModuleLocator:
       def __init__(self, page: Page):
           self.my_button = page.get_by_text("Click Me")
      

4. Write tests:
      python
   @pytest.mark.module_name
   def test_feature(authenticated_page):
       page = MyModulePage(authenticated_page)
       # Test code
   

### Fixing a Bug in Tests

1. Create bug fix branch:
      powershell
   git checkout -b fix/flaky-timeout-issue
      

2. Update code or test
3. Add test to verify fix
4. Commit with descriptive message:
   
   fix(modules): increase timeout for search results
   

### Improving Documentation

1. Update relevant markdown file
2. Verify formatting renders correctly
3. Commit:
   
   docs(readme): clarify parallel test execution
   
---

## Questions or Issues?

- **Setup problems**: Check [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Test questions**: Review test examples in [README.md](./README.md#writing-tests)
- **General help**: Open an issue with questions
- **Bugs**: Submit bug report with reproduction steps

**Last Updated**: March 18, 2026
