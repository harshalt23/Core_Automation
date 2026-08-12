# Core Automation - Project Architecture & Structure

This document provides a detailed overview of the Core Automation Framework's architecture, design patterns, and directory structure.

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Design Patterns Used](#design-patterns-used)
3. [Directory Structure](#directory-structure)
4. [Key Components](#key-components)
5. [Data Flow](#data-flow)
6. [Extension Points](#extension-points)

---

## Architecture Overview

### Framework Layers

```
┌─────────────────────────────────────────────────┐
│           Test Files (tests/)                   │
│  - test_home.py, test_analytical_plan.py, etc   │
└──────────────────┬──────────────────────────────┘
                   │ Uses
                   ▼
┌─────────────────────────────────────────────────┐
│      Page Object Models (modules/)              │
│  - Pages, Actions, Locators                     │
└──────────────────┬──────────────────────────────┘
                   │ Depends on
                   ▼
┌─────────────────────────────────────────────────┐
│  Utilities & Helpers (utils/)                   │
│  - Config, Logging, Screenshots, etc.           │
└──────────────────┬──────────────────────────────┘
                   │ Uses
                   ▼
┌─────────────────────────────────────────────────┐
│      Playwright (External Library)              │
│  - Browser Automation, Page API                 │
└─────────────────────────────────────────────────┘
```

### Execution Flow

```
1. Pytest starts
   │
2. conftest.py creates authenticated_page fixture
   │
3. Browser launches with persistent context
   │
4. Test file imports Page Object
   │
5. Test calls page methods
   │
6. Page Object interacts with browser
   │
7. Test validates results
   │
8. Browser closes, artifacts collected
```

---

## Design Patterns Used

### 1. Page Object Model (POM)

**Purpose**: Encapsulate UI interactions and make tests maintainable

**Structure**:
```
modules/
└── feature_name/
    └── pages/
        ├── feature_name.py           # Page actions (methods)
        ├── feature_name_locator.py   # Element locators
        └── __init__.py
```

**Example**:
```python
# feature_name_locator.py - Contains only locators
class FeatureLocator:
    def __init__(self, page: Page):
        self.submit_button = page.get_by_text("Submit")
        self.status_message = page.locator(".status")

# feature_name.py - Contains actions and methods
class FeaturePage:
    def __init__(self, page: Page):
        self.locator = FeatureLocator(page)
    
    def click_submit(self):
        self.locator.submit_button.click()
```

**Benefits**:
-  Changes to UI only affect locator file
-  Tests remain clean and readable
-  Easier to maintain as UI changes

### 2. Fixture Pattern (pytest)

**Purpose**: Provide setup/teardown and shared resources

**Implementation**:
```python
# conftest.py
@pytest.fixture(scope="function")
def authenticated_page(request, worker_id):
    # Create browser with auth
    # Yield page to test
    # Cleanup after test
    yield page
```

**Benefits**:
-  Automatic setup/teardown
-  Reusable across tests
-  Can be scoped (function, class, module, session)

### 3. Configuration Pattern

**Purpose**: Manage environment-specific settings

**Implementation**:
```yaml
# config/config.yaml
env: qa
environments:
  qa:
    base_url: "https://core-dev.mma.com/core_v2/ui/"
  prod:
    base_url: "https://core.mma.com/core/ui/"
```

**Usage**:
```python
# config_reader.py
config = load_config()
page.goto(config["base_url"])
```

**Benefits**:
-  No hardcoded values in code
-  Easily switch between environments
-  Secrets not in version control

### 4. Observer Pattern (Logging & Reporting)

**Purpose**: Track test execution and capture artifacts

**Components**:
- Logger: Records execution events
- Screenshot Utils: Captures on failure
- Trace Utils: Records Playwright trace
- Allure Reports: Aggregates all data

**Flow**:
```
Test starts
    ↓
Logger logs action
    ↓
Playwright executes
    ↓
Result recorded
    ↓
Artifacts collected (screenshots, traces)
    ↓
Test ends
    ↓
Reports generated
```

---

## Directory Structure

### Root Level

```
Core_Automation/
├── README.md                    # Main documentation
├── SETUP_GUIDE.md              # Detailed setup instructions
├── CONTRIBUTING.md             # Contribution guidelines
├── PROJECT_STRUCTURE.md        # This file
├── pytest.ini                  # Pytest configuration
├── conftest.py                 # Pytest fixtures
├── requirements.txt            # Python dependencies
├── run_claude.py               # Claude AI integration
├── claude_helper.py            # Claude API wrapper
└── .github/
    └── workflows/
        └── tests.yml           # GitHub Actions CI/CD
```

### Configuration (config/)

```
config/
├── __init__.py
└── config.yaml                 # Environment & browser settings

Purpose: Centralized configuration for all environments
Accessed by: config_reader.py
Used in: conftest.py, all tests
```

**config.yaml Structure**:
```yaml
env: qa                         # Current environment

environments:                   # Multi-environment setup
  qa:
    base_url: "..."
  prod:
    base_url: "..."

browser: "chromium"            # Browser type
headless: false                # UI visibility
timeouts:                      # Global timeouts
  page_load: 90000
  action_timeout: 20000
```

### Authentication (auth/)

```
auth/
├── save_login_state.py         # Script to generate auth state
└── storage_states/
    └── admin.json              # Stored login credentials

Purpose: Handle browser authentication
How it works:
1. Manual login (browser opens)
2. Credentials stored in admin.json
3. Reused by all tests via conftest.py fixture
```

### Modules (modules/)

```
modules/
├── __init__.py
├── home/
│   ├── __init__.py
│   └── pages/
│       ├── __init__.py
│       ├── home.py             # HomePage class
│       └── home_locator.py     # HomeLocator class
│
├── analytical_plan/
│   ├── __init__.py
│   └── pages/
│       ├── __init__.py
│       ├── analytical_plan.py
│       └── analytical_plan_locator.py
│
├── workbook/
│   ├── __init__.py
│   └── pages/
│       ├── __init__.py
│       ├── workbook.py
│       └── workbook_locator.py
│
└── [Other modules: analytic_dataset, project_specs, main_model, activate_input]

Purpose: Page Object Models for each feature/module
Structure:
  - One module per feature
  - pages/ subfolder contains:
    - Page class: Actions & methods
    - Locator class: Element selectors
  - __init__.py for imports

Naming Convention:
  - Page class: {FeatureName}Page
  - Locator class: {FeatureName}Locator
  - File names: snake_case (feature_name.py)
```

**Module File Contents**:

```python
# modules/feature_name/pages/feature_name_locator.py
# Contains: Element selectors only
class FeatureNameLocator:
    def __init__(self, page: Page):
        self.element1 = page.get_by_text("...")
        self.element2 = page.locator(".selector")

# modules/feature_name/pages/feature_name.py
# Contains: Page actions and methods
class FeatureNamePage:
    def __init__(self, page: Page):
        self.page = page
        self.locator = FeatureNameLocator(page)
    
    def perform_action(self):
        self.locator.element1.click()
```

### Tests (tests/)

```
tests/
├── __init__.py
├── home/
│   ├── __init__.py
│   └── test_home.py            # Home page tests
│
├── analytical_plan/
│   ├── __init__.py
│   └── test_analytical_plan.py
│
├── sanity/
│   ├── __init__.py
│   └── test_basic_launch.py    # Smoke tests
│
├── e2e/
│   ├── __init__.py
│   └── test_full_core_workflow.py  # End-to-end scenarios
│
├── workbook/
├── analytic_dataset/
├── project_specs/
├── main_model/
├── activate_input/
│
└── test_suite.py               # Optional: Master test suite

Purpose: Pytest test files
Organization:
  - Mirror modules/ structure
  - One test file per feature
  - Related tests grouped in classes

Test Organization Pattern:
  - Smoke tests: Quick sanity checks (tests/sanity/)
  - Module tests: Feature-specific (tests/module_name/)
  - E2E tests: Full workflows (tests/e2e/)
```

**Test File Template**:
```python
# tests/feature_name/test_feature_name.py
import pytest
from modules.feature_name.pages.feature_name import FeatureNamePage

@pytest.mark.smoke
@pytest.mark.module_feature_name
class TestFeatureName:
    """Test suite for Feature Name module"""
    
    def test_feature_loads(self, authenticated_page):
        """Verify feature page loads successfully"""
        page_obj = FeatureNamePage(authenticated_page)
        # Test code
```

### Utilities (utils/)

```
utils/
├── __init__.py
├── auth.py                 # Authentication helper
├── base_page.py            # Base page class (abstract)
├── config_reader.py        # Load configuration
├── logger_utils.py         # Logging setup
├── screenshot_utils.py     # Screenshot capture
├── trace_utils.py          # Playwright trace recording
├── folder_utils.py         # Folder creation/cleanup
├── helpers.py              # Utility functions
└── __pycache__/

Purpose: Shared utilities and helpers

File Purposes:

1. base_page.py
   - Abstract base class for all Page Objects
   - Common methods (waits, clicks, fills)
   - Shared logging

2. config_reader.py
   - Loads config.yaml
   - Validates configuration
   - Provides config to tests

3. logger_utils.py
   - Sets up logging
   - Configures log files
   - Adds console & file handlers

4. auth.py
   - Browser authentication setup
   - Storage state management
   - Login flow handling

5. screenshot_utils.py
   - Captures screenshots on demand
   - Generates timestamped filenames
   - Stores in reports/screenshots/

6. trace_utils.py
   - Starts Playwright trace
   - Records interactions
   - Stores as ZIP file

7. folder_utils.py
   - Creates report directories
   - Cleanup operations
   - Path management

8. helpers.py
   - General utility functions
   - Data helpers
   - Common operations
```

### Reports (reports/) - Auto-generated

```
reports/
├── report.html              # Pytest HTML report
├── allure-results/          # Allure test data
│   ├── *.json              # Test results
│   └── environment.properties
│
├── screenshots/            # Screenshots on failure
│   ├── test_name_timestamp.png
│   └── ...
│
├── traces/                 # Playwright traces
│   ├── test_name_timestamp.zip
│   └── ...
│
├── videos/                 # Record video (if enabled)
│   └── ...
│
└── logs/
    └── execution.log       # Detailed execution log

Purpose: Store test artifacts
Auto-created by: conftest.py & utils
Accessed by: CI/CD, Manual review
```

### Browser Profile (edge_profile/) - Auto-created

```
edge_profile/
├── Default/                # Microsoft Edge profile
│   ├── Cookies
│   ├── Cache
│   └── ...
├── BrowserMetrics/
└── ...

Purpose: Persistent Edge browser data
Contents: Cache, cookies, history
Created by: conftest.py fixture

Note: In parallel runs, creates edge_profile_gw0, edge_profile_gw1, etc.
      Automatically cleaned up after tests
```

---

## Key Components

### 1. conftest.py - Test Configuration

**Purpose**: Pytest configuration and fixtures

**Key Fixtures**:
```python
@pytest.fixture(scope="session", autouse=True)
def environment_details():
    # Generate environment.properties for Allure

@pytest.fixture(scope="function")
def authenticated_page(request, worker_id):
    # Launch browser with authentication
    # Provides logged-in page to tests
    # Handles cleanup and artifact collection
```

**Key Functions**:
```python
def cleanup_parallel_profiles():
    # Remove worker-specific profiles (gw0, gw1, etc.)

@pytest.fixture(scope="session", autouse=True)
def environment_details():
    # Generate environment properties for Allure
```

### 2. requirements.txt - Dependencies

**Categories**:

1. **Core Testing**:
   - pytest: Test framework
   - pytest-playwright: Playwright integration
   - playwright: Browser automation

2. **Parallel Execution**:
   - pytest-xdist: Parallel test runner
   - execnet: Communication between workers

3. **Reporting**:
   - pytest-html: HTML reports
   - allure-pytest: Allure integration

4. **Utilities**:
   - python-dotenv: Environment variables
   - PyYAML: YAML config parsing
   - anthropic: Claude AI API

### 3. pytest.ini - Pytest Configuration

**Key Settings**:
```ini
[pytest]
addopts = -ra --clean-alluredir --html=reports/report.html
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
log_cli = true
markers = smoke, regression, module_*
```

---

## Data Flow

### Test Execution Flow

```
1. START pytest
   ↓
2. Load pytest.ini
   ↓
3. Load conftest.py
   ↓
4. Create environment_details (session fixture)
   ↓
5. For each test:
   ├─ Load Test file
   ├─ Create authenticated_page fixture
   │  ├─ Load config
   │  ├─ Launch browser
   │  ├─ Navigate to base_url
   │  └─ Return page object
   │
   ├─ Run test
   │  ├─ Import Page Object
   │  ├─ Execute test code
   │  └─ Assert results
   │
   ├─ Collect artifacts
   │  ├─ Screenshot (if failed)
   │  ├─ Trace replay
   │  └─ Logs
   │
   └─ Cleanup fixture
      ├─ Stop trace
      ├─ Close browser
      └─ Save state
   ↓
6. Generate reports
   ├─ HTML report (reports/report.html)
   ├─ Allure results
   └─ Summary
   ↓
7. END
```

### Configuration Loading Flow

```
Test starts
    ↓
config_reader.py.load_config() called
    ↓
Load config/config.yaml
    ↓
Get env from yaml (qa, prod, etc.)
    ↓
Extract base_url for environment
    ↓
Return config dict
    ↓
Used in conftest.py fixture
    ↓
Browser navigates to base_url
```

### Authentication Flow

```
First Run:
    python auth/save_login_state.py
    ↓
    Browser opens
    ↓
    Manual login (with phone approval)
    ↓
    Storage state saved to admin.json

Subsequent Runs:
    conftest.py loads authenticated_page fixture
    ↓
    Reads auth/storage_states/admin.json
    ↓
    Creates context with stored auth state
    ↓
    User automatically logged in
    ↓
    Tests execute as authenticated user
```

---

## Extension Points

### Adding a New Module

**Steps**:
1. Create directory: `modules/new_module/pages/`
2. Create locator class: `modules/new_module/pages/new_module_locator.py`
3. Create page class: `modules/new_module/pages/new_module.py`
4. Create test directory: `tests/new_module/`
5. Create test file: `tests/new_module/test_new_module.py`
6. Add pytest marker in `pytest.ini`: `module_new_module`

### Adding New Utilities

**Location**: `utils/`

**Template**:
```python
# utils/my_utility.py
"""
Utility module for [purpose]

Used by: [which modules use this]
Dependencies: [external dependencies]
"""

def my_helper_function(param: str) -> str:
    """Helper function description."""
    pass
```

### Adding New Fixtures

**Location**: `conftest.py`

**Template**:
```python
@pytest.fixture(scope="function")
def my_fixture():
    """Description of fixture."""
    # Setup
    resource = setup()
    
    yield resource
    
    # Teardown
    cleanup()
```

### Custom pytest Hooks

**Location**: `conftest.py`

**Examples**:
```python
def pytest_runtest_makereport(item, call):
    """Hook called after each test"""
    pass

def pytest_collection_modifyitems(config, items):
    """Hook to modify collected tests"""
    pass

def pytest_addoption(parser):
    """Hook to add custom command line options"""
    pass
```

---

## Design Principles

### DRY (Don't Repeat Yourself)
- Use base classes for common functionality
- Reuse page objects across tests
- Extract common waits/actions

### KISS (Keep It Simple, Stupid)
- One class does one thing
- Clear, readable names
- Simple logic > complex logic

### SOLID Principles
- **S**ingle Responsibility: One class = one concern
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Page objects are interchangeable
- **I**nterface Segregation: Small focused interfaces
- **D**ependency Inversion: Depend on abstractions

---

## Performance Considerations

### Load Time Optimization
```python
# Use specific waits, not hard waits
element.wait_for(state="visible")  #  Good
page.wait_for_timeout(5000)        #  Bad
```

### Browser Profile Management
- Persistent profiles reduce login time
- Parallel execution uses separate profiles
- Auto-cleanup prevents disk space issues

### Parallel Execution
```powershell
pytest -n auto              # Use all CPU cores
pytest -n 4 --dist loadscope  # 4 workers, parallel by scope
```

---

## Testing Best Practices

1. **Isolation**: Each test should be independent
2. **Clarity**: Test name describes what it tests
3. **Assertions**: Multiple specific assertions > one generic
4. **Logging**: Log important steps for debugging
5. **Cleanup**: Always clean up created data

---

## Future Enhancements

Potential improvements to the architecture:

1. **Base Page Class**: Extract common methods for all pages
2. **Custom Assertions**: Create assertion helpers
3. **Data Fixtures**: Centralize test data management
4. **Mock API**: Mock backend for unit-like tests
5. **Performance Benchmarking**: Track test execution times
6. **Video Recording**: Capture videos on failure

---

**Last Updated**: March 18, 2026  
**Framework Version**: 1.0.0
