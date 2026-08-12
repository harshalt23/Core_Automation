# Core Automation Framework

A comprehensive Playwright-based test automation framework for the Core application. Built with Python, pytest, and integrated with Allure reporting for advanced test analytics.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Writing Tests](#writing-tests)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)

---

## Overview

The **Core Automation Framework** is designed for end-to-end testing of the Core application with the following features:

 **Page Object Model (POM)** - Maintainable and scalable test structure  
 **Parallel Test Execution** - Run multiple tests simultaneously with pytest-xdist  
 **Advanced Reporting** - Allure reports with traces, screenshots, and videos  
 **AI-Powered Debugging** - Claude integration for analyzing and fixing test failures  
 **Multi-Environment Support** - QA, Prod, and custom environment configurations  
 **Browser Profiles** - Persistent Edge browser context with authentication state  
 **Comprehensive Logging** - Detailed execution logs for debugging  

---

## Prerequisites

### System Requirements
- **OS**: Windows 10/11 (or Linux/macOS with adjustments)
- **Python**: 3.9 or higher
- **Edge Browser**: Microsoft Edge installed (used for automation)
- **Java** (Optional): Required for Allure report generation

### Install Python (if not already installed)
1. Download from [python.org](https://www.python.org/downloads/)
2. Install with "Add Python to PATH" checked
3. Verify: `python --version`

### Install Edge Browser
- Download from [Microsoft Edge](https://www.microsoft.com/en-us/edge)

### Install Java (for Allure reports, optional)
- Download from [Java.com](https://www.java.com/en/download/)
- Required for: `allure serve` command to generate HTML reports

---

## Installation & Setup

### Step 1: Clone or Download the Repository

```powershell
# Navigate to your workspace directory
cd C:\Users\<YourUsername>\Core_Automation

# Verify the folder structure exists
Get-ChildItem
```

### Step 2: Create a Python Virtual Environment

A virtual environment isolates project dependencies.

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
# Ensure pip is updated
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Install Playwright browsers (Downloads Edge, Chrome, Firefox)
playwright install
```

### Step 4: Create Browser Profile for Authentication

The framework uses a persistent Edge profile to store authentication state.

```powershell
# From the project root directory
cd Core_Automation

# Run the authentication setup script
python auth/save_login_state.py

# Follow prompts:
# 1. Browser opens automatically
# 2. Login manually using Microsoft Authenticator
# 3. Complete phone approval
# 4. Press ENTER in terminal when done
```

This creates `auth/storage_states/admin.json` - used by all tests for authentication.

### Step 5: Verify Installation

```powershell
# Run a quick sanity test
pytest tests/sanity/test_basic_launch.py -v

# Expected output: PASSED
```

---

## Configuration

### Modify Environment & URL

Edit `Core_Automation/config/config.yaml`:

```yaml
env: qa                    # Change to 'prod' for production testing

environments:
  qa:
    base_url: "https://core-dev.mma.com/core_v2/ui/"
  
  prod:
    base_url: "https://core.mma.com/core/ui/"

browser: "chromium"        # Options: chromium, firefox, webkit
headless: false            # Set to true to run without UI

timeouts:
  page_load: 90000        # 90 seconds to wait for page load
  action_timeout: 20000   # 20 seconds for element interactions
```

### Switch Environment

```powershell
# For QA (default)
pytest tests/ -m smoke

# For Production (change config.yaml first)
# Edit config.yaml: env: prod
pytest tests/ -m regression
```

---

## Running Tests

### Run All Tests

```powershell
# Run entire test suite with HTML report
pytest

# View HTML report
start reports/report.html
```

### Run by Test Category (Markers)

```powershell
# Smoke tests (quick sanity checks)
pytest -m smoke

# Regression tests (full suite)
pytest -m regression

# Module-specific tests
pytest -m module_ap      # Analytical Plan tests
pytest -m module_wb      # Workbook tests
pytest -m module_ads     # Analytic Dataset tests
pytest -m module_mm      # Main Model tests
pytest -m module_ps      # Project Specs tests
pytest -m module_ai      # Activate Input tests
```

### Run Specific Test File or Function

```powershell
# Single test file
pytest tests/home/test_home.py

# Single test function
pytest tests/home/test_home.py::test_home_page_load -v

# Tests matching a pattern
pytest -k "home" -v
```

### Run Tests in Parallel

Run multiple tests simultaneously to save time:

```powershell
# Run with 4 workers (adjust based on CPU cores)
pytest -n 4 --dist loadscope

# Run with automatic worker detection
pytest -n auto
```

### Generate Allure Reports

Allure reports provide detailed test execution analytics:

```powershell
# Generate Allure report with history
allure serve reports/allure-results

# Generate static report (without Java)
allure generate reports/allure-results

# View static report
start allure-report/index.html
```

### View HTML Report

```powershell
# HTML report with all details
start reports/report.html

# Video recordings (if videos enabled)
start reports/videos/

# Screenshots on failure
start reports/screenshots/

# Execution logs
start reports/logs/execution.log
```

### Common Pytest Options

```powershell
# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run failed tests first, then others
pytest --ff

# Retry failed tests (2 times)
pytest --reruns 2

# Show slowest 5 tests
pytest --durations=5
```

---

## Project Structure

```
Core_Automation/
├── config/
│   ├── __init__.py
│   └── config.yaml                 # Environment and browser configuration
│
├── auth/
│   ├── storage_states/
│   │   └── admin.json             # Stored login credentials
│   └── save_login_state.py        # Script to generate storage_state.json
│
├── modules/                         # Page Object classes organized by feature
│   ├── home/
│   │   └── pages/
│   │       ├── home.py            # HomePage class with methods
│   │       └── __init__.py
│   ├── analytical_plan/
│   │   └── pages/
│   │       ├── analytical_plan.py # AnalyticalPlanPage class
│   │       ├── analytical_plan_locator.py  # Locators for elements
│   │       └── __init__.py
│   ├── workbook/
│   ├── analytic_dataset/
│   ├── project_specs/
│   ├── main_model/
│   └── activate_input/
│
├── tests/                           # Test files organized by module
│   ├── home/
│   │   ├── test_home.py           # Home page tests
│   │   └── __init__.py
│   ├── analytical_plan/
│   │   ├── test_analytical_plan.py
│   │   └── __init__.py
│   ├── e2e/
│   │   ├── test_full_core_workflow.py  # End-to-end tests
│   │   └── __init__.py
│   ├── sanity/
│   │   ├── test_basic_launch.py   # Basic smoke tests
│   │   └── __init__.py
│   ├── workbook/
│   ├── analytic_dataset/
│   ├── project_specs/
│   ├── main_model/
│   ├── activate_input/
│   ├── test_suite.py              # Master test suite (optional)
│   └── __init__.py
│
├── utils/                           # Shared utilities
│   ├── auth.py                    # Authentication helper
│   ├── base_page.py               # Base page class with common methods
│   ├── config_reader.py           # Config loader
│   ├── logger_utils.py            # Logging setup
│   ├── screenshot_utils.py        # Screenshot capture
│   ├── trace_utils.py             # Playwright trace recording
│   ├── folder_utils.py            # Folder creation/cleanup
│   ├── helpers.py                 # Common utility functions
│   └── __init__.py
│
├── reports/                         # Test reports and artifacts (auto-generated)
│   ├── report.html                # Pytest HTML report
│   ├── allure-results/            # Allure report data
│   ├── screenshots/               # Screenshots on failure
│   ├── traces/                    # Playwright traces for debugging
│   ├── videos/                    # Video recordings
│   └── logs/
│       └── execution.log          # Detailed execution logs
│
├── edge_profile/                    # Edge browser profile (auto-created)
│   └── Default/
│       └── Cookies, cache, history...
│
├── requirements.txt               # Python dependencies
├── pytest.ini                     # Pytest configuration
├── conftest.py                    # Pytest fixtures and hooks
├── run_claude.py                  # Claude AI helper for test debugging
├── claude_helper.py               # Claude API integration
├── structure.txt                  # Project structure documentation
└── README.md                      # This file
```

---

## Writing Tests

### Test Naming Convention

```python
# File: tests/module_name/test_feature.py
# Function: test_<action>_<expected_result>

def test_user_can_login_successfully(authenticated_page):
    """Verify user can login with valid credentials"""
    pass

def test_search_returns_matching_projects(authenticated_page):
    """Verify search returns only matching project names"""
    pass
```

### Test Structure (Given-When-Then)

```python
from modules.home.pages.home import HomePage

@pytest.mark.smoke
@pytest.mark.module_home
def test_expand_project_from_home(authenticated_page):
    """
    GIVEN: User is on Home page
    WHEN: User searches for a project and expands it
    THEN: Project details should be visible
    """
    # GIVEN
    home = HomePage(authenticated_page)
    home.wait_for_home_to_load()
    
    # WHEN
    home.search_project("Core QA Only")
    home.expand_project("Core QA Only")
    
    # THEN
    assert "Core QA Only" in authenticated_page.content()
    assert home.is_project_expanded("Core QA Only")
```

### Adding Test Markers

```python
# In pytest.ini (already configured)
markers =
    smoke: small set of critical tests
    regression: full regression suite
    module_ap: Analytic Plan Module tests
    # Add more as needed

# Apply to test
@pytest.mark.smoke
@pytest.mark.module_ap
def test_create_analytical_plan(authenticated_page):
    pass
```

### Creating a New Test Module

```
tests/
└── new_feature/
    ├── __init__.py
    └── test_new_feature.py

# In test_new_feature.py
import pytest
from modules.new_feature.pages.new_feature_page import NewFeaturePage

@pytest.mark.smoke
def test_new_feature_loads(authenticated_page):
    feature = NewFeaturePage(authenticated_page)
    feature.verify_page_loaded()
```

### Using Fixtures

```python
# Built-in fixture provided by conftest.py
def test_my_test(authenticated_page):
    """authenticated_page is a fixture providing logged-in Playwright Page"""
    authenticated_page.goto("https://example.com")
    assert "Example" in authenticated_page.title()

# Custom fixture example
@pytest.fixture
def test_data():
    return {
        "project": "Test Project",
        "database": "Test DB"
    }

def test_with_data(authenticated_page, test_data):
    project_name = test_data["project"]
    # Use project_name in test
```

---

## Best Practices

### 1. Use Page Object Model (POM)

 **Good**:
```python
# pages/my_page.py
class MyPage:
    def __init__(self, page: Page):
        self.page = page
    
    def fill_search(self, text: str):
        search_box = self.page.locator("input[placeholder='Search']")
        search_box.fill(text)

# tests/test_my_feature.py
def test_search(authenticated_page):
    my_page = MyPage(authenticated_page)
    my_page.fill_search("test query")
```

 **Bad**:
```python
def test_search(page):
    page.locator("input[placeholder='Search']").fill("test query")
    page.locator("button:text('Search')").click()
```

### 2. Use Explicit Waits

 **Good**:
```python
element = page.get_by_text("Expected Text")
element.wait_for(state="visible", timeout=5000)
element.click()
```

 **Bad**:
```python
page.wait_for_timeout(5000)  # Hard wait!
page.get_by_text("Expected Text").click()
```

### 3. Add Descriptive Assertions

 **Good**:
```python
assert "Success" in page.content(), "Success message should appear after save"
assert page.url.startswith("https://core"), "Should redirect to core app"
```

 **Bad**:
```python
assert "Success" in page.content()
assert len(page.content()) > 0
```

### 4. Use Logging for Debugging

```python
import logging

logger = logging.getLogger(__name__)

class MyPage:
    def fill_search(self, text: str):
        logger.info(f"Searching for: {text}")
        try:
            search_box = self.page.locator("input[placeholder='Search']")
            search_box.fill(text)
            logger.info(f"Successfully filled search with: {text}")
        except Exception as e:
            logger.error(f"Failed to fill search: {str(e)}")
            raise
```

### 5. Handle Dynamic Timeouts

```python
# Instead of hard-coded 5000ms
def wait_for_element(self, locator, timeout=None):
    if timeout is None:
        timeout = self.page.context.timeout  # Use config timeout
    locator.wait_for(state="visible", timeout=timeout)
```

### 6. Clean Up Browser Profile

```python
# conftest.py already handles cleanup
@pytest.fixture(scope="function")
def authenticated_page(request, worker_id):
    # Browser profile is cleaned up after each test
    # Parallel profiles (gw0, gw1, etc.) are removed
    yield page
```

### 7. Use Allure Annotations

```python
import allure

@allure.feature("Home Page")
@allure.story("Project Search")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_project(authenticated_page):
    pass

# View in Allure report
```

---

## Troubleshooting

### Issue: "playwright: command not found"

**Solution**:
```powershell
pip install playwright
playwright install
```

---

### Issue: Tests fail with "TimeoutError: Timeout 30000ms exceeded"

**Common causes**:
1. Element doesn't exist on page
2. Element is hidden or not visible
3. Application is slow to load

**Debugging steps**:
```powershell
# 1. Check screenshots of failed test
start reports/screenshots/

# 2. View Playwright trace
allure serve reports/allure-results/

# 3. Check execution logs
Get-Content reports/logs/execution.log -Tail 100

# 4. Increase timeout in config.yaml
# timeouts:
#   action_timeout: 30000  # Increase from 20000
```

---

### Issue: "Cannot find Edge browser" or "Channel 'msedge' is not installed"

**Solution**:
```powershell
# Reinstall Playwright browsers
playwright install

# Or install Edge specifically
playwright install msedge
```

---

### Issue: Tests pass locally but fail in CI/CD

**Common causes**:
1. Different OS (Windows vs Linux)
2. Missing environment variables
3. Authentication state not persisted

**Solution**:
```powershell
# Ensure auth storage is committed to repo
git add auth/storage_states/

# Set environment-specific config in CI
# Create environment variable: TEST_ENV=qa
```

---

### Issue: Parallel tests fail with "edge_profile locked" error

**Solution**:
```powershell
# Remove locked profiles
Remove-Item edge_profile_gw* -Recurse -Force

# conftest.py auto-cleanup should handle this
# If issue persists, reduce parallel workers:
pytest -n 2  # Use 2 workers instead of auto
```

---

### Issue: "FAILED - Cannot log in / Auth state missing"

**Solution**:
```powershell
# Regenerate authentication
python auth/save_login_state.py

# Delete corrupted storage state
Remove-Item auth/storage_states/admin.json

# Create new one and commit to repo
```

---

### Issue: Allure report shows "No test results"

**Solution**:
```powershell
# Ensure Allure results are generated
pytest --alluredir=reports/allure-results

# Check if Java is installed (required for allure serve)
java -version

# If Java not installed:
# Download from https://www.java.com/en/download/

# Generate report without Java
allure generate reports/allure-results -o allure-report
start allure-report/index.html
```

---

### Issue: "ModuleNotFoundError: No module named 'modules'"

**Solution**:
```powershell
# Run pytest from project root
cd Core_Automation
pytest

# Or add root to Python path
pytest --rootdir=.
```

---

### Issue: Tests run slow / Browser takes long to start

**Optimization**:
```python
# conftest.py - Reduce slow_mo
context = playwright.chromium.launch_persistent_context(
    headless=False,
    slow_mo=500  # Reduce from 1000 to 500ms
)

# Or disable for faster runs (less visual feedback)
slow_mo=0
```

---

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Core Automation Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  test:
    runs-on: windows-latest
    
    strategy:
      matrix:
        python-version: ['3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        playwright install
    
    - name: Run smoke tests
      run: |
        pytest -m smoke --alluredir=allure-results
    
    - name: Generate Allure Report
      if: always()
      uses: simple-elf/allure-report-action@master
      with:
        allure_results: allure-results
        allure_history: allure-history
        keep_reports: 20
    
    - name: Upload artifacts
      if: failure()
      uses: actions/upload-artifact@v3
      with:
        name: test-artifacts
        path: reports/
```

---

## Contributing

### Adding a New Test

1. **Create test file** in appropriate module:
   ```
   tests/module_name/test_feature.py
   ```

2. **Create page object** if testing new UI:
   ```
   modules/module_name/pages/feature_page.py
   ```

3. **Follow test structure**:
   ```python
   @pytest.mark.smoke
   @pytest.mark.module_name
   def test_feature_works(authenticated_page):
       """Descriptive docstring"""
       # Arrange
       page = MyPage(authenticated_page)
       
       # Act
       page.do_something()
       
       # Assert
       assert expected_result
   ```

4. **Run and verify**:
   ```powershell
   pytest tests/module_name/test_feature.py -v
   ```

5. **Commit changes**:
   ```powershell
   git add tests/module_name/
   git commit -m "Add test for feature X"
   ```

### Code Quality

- Use meaningful variable names
- Add docstrings to functions and classes
- Keep tests focused on one behavior
- Reuse page objects instead of duplicating element locators
- Document complex selectors with comments

---

## Additional Resources

- **Playwright Docs**: https://playwright.dev/python/
- **Pytest Docs**: https://docs.pytest.org/
- **Allure Docs**: https://docs.qameta.io/allure/
- **Page Object Model**: https://martinfowler.com/bliki/PageObject.html

---

## Support & Contact

For issues, questions, or contributions:

1. Check [Troubleshooting](#troubleshooting) section
2. Review test logs: `reports/logs/execution.log`
3. View Allure reports: `allure serve reports/allure-results`
4. Contact: [Team Name/Contact Info]

---

**Last Updated**: March 18, 2026  
**Framework Version**: 1.0.0  
**Python Version**: 3.9+  
**Playwright Version**: 1.58.0+
