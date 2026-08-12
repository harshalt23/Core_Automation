# Core Automation - FAQ & Troubleshooting Guide

Comprehensive Q&A and solutions for common issues encountered while using the Core Automation Framework.

## Table of Contents
1. [Installation & Setup FAQs](#installation--setup-faqs)
2. [Running Tests FAQs](#running-tests-faqs)
3. [Test Failures & Debugging](#test-failures--debugging)
4. [Performance Issues](#performance-issues)
5. [Reporting Issues](#reporting-issues)
6. [Advanced Topics](#advanced-topics)

---

## Installation & Setup FAQs

### Q: How do I know if Python is installed correctly?

**A:** Run these commands:
```powershell
python --version      # Should show: Python 3.9.x or higher
pip --version         # Should show: pip 21.x or higher
python -m venv test   # Should create test folder
```

If any fails, reinstall Python from https://python.org with "Add Python to PATH" checked.

---

### Q: What's the difference between venv and global Python?

**A:** 
- **Global Python**: System-wide installation
- **venv**: Project-specific virtual environment

**Why use venv?**
-  Isolates project dependencies
-  Prevents conflicts between projects
-  Easy to cleanup (just delete venv folder)
-  Required for CI/CD pipelines

**Recommendation**: Always use venv for development.

---

### Q: I got "ExecutionPolicy" error when activating venv

**A:** PowerShell doesn't allow running scripts by default.

```powershell
# Fix it once (for current user)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\venv\Scripts\Activate.ps1

# You should see (venv) at terminal start
```

---

### Q: How do I install Playwright browsers?

**A:** Run:
```powershell
# Install all browsers (Chromium, Firefox, WebKit)
playwright install

# Or install Edge only (faster)
playwright install msedge

# Verify installation
playwright install --help
```

**Common issues**:
- Takes 5-10 minutes on first run
- Requires ~1GB disk space
- Needs internet connection

---

### Q: How do I set up authentication?

**A:** Follow these steps:

```powershell
# 1. Navigate to project
cd Core_Automation\Core_Automation

# 2. Run auth setup script
python ..\auth\save_login_state.py

# 3. Browser opens automatically
# 4. Login manually:
#    - Enter credentials OR
#    - Complete Microsoft Authenticator flow
#
# 5. Once logged in successfully, press ENTER in terminal

# 6. Verify admin.json was created
Test-Path ..\auth\storage_states\admin.json
```

**What happens?**
- Browser opens to login page
- You login manually (simulates real user)
- Credentials saved to `admin.json`
- All tests use saved credentials

**If manual browser doesn't open**:
```powershell
# Run script, then paste URL in browser manually
python ..\auth\save_login_state.py
# Copy this URL when prompted:
# https://core-dev.mma.com/core_v2/ui/
```

---

### Q: Can I commit auth/storage_states/admin.json to git?

**A:** Yes, but be careful:
-  Safe: If credentials are temporary/test accounts
-  Risky: If credentials are production/real accounts
-  Never: Commit real production credentials

**Recommendation**: Use separate auth files for different environments:
```
auth/storage_states/
├── admin.json          # Test account
├── admin_prod.json     # Production (don't commit!)
└── guest.json          # Guest account
```

---

### Q: How do I reset everything and start fresh?

**A:**
```powershell
# 1. Stop any running tests
# (Ctrl+C in terminal)

# 2. Deactivate virtual environment
deactivate

# 3. Remove everything
Remove-Item -Recurse -Force venv
Remove-Item -Recurse -Force .pytest_cache
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force reports
 Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force # to delete the __pycache__ folders

# 4. Reinstall from scratch
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install

cd Core_Automation\Core_Automation
python ..\auth\save_login_state.py
```

---

## Running Tests FAQs

### Q: How do I run just smoke tests?

**A:**
```powershell
pytest -m smoke -v

# This runs only tests marked with @pytest.mark.smoke
```

---

### Q: What's the difference between smoke, regression, and other markers?

**A:**
| Marker | Purpose | Runtime | Frequency |
|--------|---------|---------|-----------|
| `@pytest.mark.smoke` | Quick sanity tests | 2-5 min | Every commit |
| `@pytest.mark.regression` | Full test suite | 30+ min | Nightly/weekly |
| `@pytest.mark.module_ap` | Specific module | Varies | As needed |
| `@pytest.mark.e2e` | Full workflows | 10+ min | Daily |

---

### Q: How do I run tests in parallel?

**A:**
```powershell
# Auto-detect CPU cores
pytest -n auto

# Specific number of workers
pytest -n 4

# By test scope (safer)
pytest -n 4 --dist loadscope

# View worker assignment
# Terminal shows: [gw0] [gw1] [gw2] [gw3]
```

**When to use parallel?**
-  Local development (faster feedback)
-  CI/CD pipelines (save time)
-  Debugging (use single worker: `-n 1`)

---

### Q: Can I run a specific test?

**A:** Yes, multiple ways:

```powershell
# Entire test file
pytest tests/home/test_home.py

# Single test function
pytest tests/home/test_home.py::test_home_page_load

# Tests matching pattern
pytest -k "search"  # All tests with "search" in name

# Combine multiple filters
pytest tests/home/ -k "load" -v
```

---

### Q: How do I see print() output in tests?

**A:**
```powershell
# -s flag shows captured output
pytest -s

# Combined with other flags
pytest tests/home/test_home.py -v -s

# Now all print() statements will display
```

### Q: What does "-x" flag do?

**A:** Stops on first failure:
```powershell
pytest -x  # Stop at first FAILED test

# Useful for: Debugging one issue at a time
# vs. running all and seeing multiple failures

---

### Q: I want to retry failed tests. How?

**A:**
   powershell
# Retry failed tests 2 times
pytest --reruns 2

# Retry with 1 second delay between
pytest --reruns 2 --reruns-delay 1

# Run last failed tests
pytest --lf

# Run failed tests first, then others
pytest --ff

**When to use?**
-  Network flakiness
-  Browser timing issues
-  Don't hide real bugs - fix root cause!

---

## Test Failures & Debugging

### Q: My test fails with "TimeoutError: Timeout 30000ms exceeded"

**A:** The element didn't appear within timeout. Debug steps:

   powershell
# 1. Check what element is missing
# Run with verbose output
pytest tests/my_test.py -v -s

# 2. View screenshot of failure
start reports/screenshots\

# 3. Check execution logs
Get-Content reports\logs\execution.log -Tail 50

# 4. Increase timeout in config.yaml
# timeouts:
#   action_timeout: 30000  # Increase from 20000

# 5. Or increase for specific element
element.wait_for(state="visible", timeout=10000)

# 6. Re-run test
pytest tests/my_test.py -v

**Common causes**:
- Element doesn't exist
- Wrong locator selector
- Application is slow
- Element hidden behind overlay
- Page hasn't loaded yet

---

### Q: Test failed with "Cannot find element" but I can see it visually

**A:** The locator is wrong. Debug:

   powershell
# 1. Open page in browser manually
# 2. Right-click element → Inspect
# 3. Check the HTML structure
# 4. Verify your locator matches

# Example - if HTML is:
# <button class="submit-btn">Submit</button>

# Try these locators:
page.get_by_text("Submit")
page.get_by_role("button", name="Submit")
page.locator(".submit-btn")
page.locator("button:has-text('Submit')")

# Best: Use page.get_by_* methods (more stable)

---

### Q: How do I use Playwright Trace for debugging?

**A:**
   powershell
# 1. Traces are auto-recorded on failures
# 2. Find trace file
dir reports\traces\

# 3. Download and open with Playwright Inspector
# On local machine:
npm install -g @playwright/test

# 4. Or view in Allure report
pytest --alluredir=reports\allure-results
allure serve reports\allure-results

**Trace shows**:
- Screenshots of each action
- DOM snapshots
- Network activity
- Exact timing

---

### Q: Test passes locally but fails in CI/CD

**A:** Common causes and solutions:

| Cause | Solution |
|-------|----------|
| Different OS | Test on both Windows/Linux |
| Missing dependencies | Update requirements.txt |
| Timing issues (CI faster) | Increase timeouts for CI |
| Environment difference | Use different config for CI |
| Missing auth state | Ensure admin.json is committed |

   powershell
# Test locally with CI settings
pytest tests/sanity/test_basic_launch.py -v

# Then run in CI/CD and compare results

---

### Q: How do I debug a specific failing test?

**A:**
   powershell
# Step 1: Run single test with verbose output
pytest tests/failing_test.py::test_name -v -s

# Step 2: Review the output for error messages

# Step 3: Check screenshots
start reports\screenshots\

# Step 4: Check logs
Get-Content reports\logs\execution.log

# Step 5: Add debug print statements
def test_something(authenticated_page):
    print("Starting test")
    page = MyPage(authenticated_page)
    print(f"Page loaded: {authenticated_page.url}")
    
    # Run with -s to see prints
    # pytest -s

# Step 6: Use breakpoints (with debugger)
import pdb
pdb.set_trace()  # Execution pauses here

---

### Q: Need more detailed debugging?

**A:** Use Allure reports:
   powershell
# Generate detailed report
pytest tests/failing_test.py --alluredir=reports\allure-results

# View in dashboard
allure serve reports\allure-results

# In Allure, you can see:
# - Step-by-step execution
# - Attachments (screenshots, traces)
# - Environment details
# - Execution timeline

---

## Performance Issues

### Q: Tests are running very slowly

**A:** Check these:

1. **Reduce `slow_mo`** in conftest.py:
      python
   # Change from:
   slow_mo=1000  # 1 second delay per action
   # To:
   slow_mo=500   # 0.5 second delay
   
2. **Use parallel execution**:
      powershell
   pytest -n auto  # Can reduce time by 60%+

3. **Reduce waits**:
      python
   # Don't use hard waits
   page.wait_for_timeout(5000)  #  BAD
   
   # Use dynamic waits
   element.wait_for(state="visible")  #  GOOD
   
4. **Check browser profile**:
      powershell
   # Profile might be corrupted
   Remove-Item edge_profile -Recurse -Force
   # Browser will recreate on next run


5. **Disable headless**:
      yaml
   # In config.yaml
   headless: true   #  Headless faster for CI
   headless: false  # For debugging locally

---

### Q: Browser takes forever to start

**A:**
   powershell
# Check if ports are in use
netstat -ano | findstr 3000  # Check port 3000

# Or reduce startup overhead
# Use headless mode:
# config.yaml: headless: true

# Or reuse browser context:
# conftest.py: scope="session" (not recommended for most cases)

---

### Q: Parallel tests sometimes fail

**A:** Common issues with parallel execution:

   powershell
# Issue: "edge_profile locked"
# Solution: Remove old profiles
Remove-Item edge_profile_gw* -Recurse -Force

# Issue: Port conflicts
# Solution: Reduce workers
pytest -n 2  # Use 2 instead of 4

# Issue: Resource contention
# Solution: Use loadscope
pytest -n 4 --dist loadscope

---

## Reporting Issues

### Q: HTML report shows no results

**A:**
   powershell
# Check if report was generated
Test-Path reports\report.html

# If not, create directory
mkdir reports\screenshots
mkdir reports\traces
mkdir reports\logs

# Run tests again
pytest

# Report should be generated now
start reports\report.html

---

### Q: Allure report shows "No test results"

**A:**
   powershell
# Check if Java is installed
java -version

# If not installed:
# Download from https://www.java.com

# Install Java, then:
allure serve reports\allure-results

# Or generate without Java
allure generate reports\allure-results -o allure-report
start allure-report\index.html
---

### Q: Screenshots not captured on failure

**A:**
   powershell
# Create screenshots directory
mkdir reports\screenshots

# Verify in conftest.py
# screenshot_utils.py should have:
def capture_screenshot(page, test_name):
    screenshot_path = f"reports/screenshots/{test_name}_{timestamp}.png"
    page.screenshot(path=screenshot_path)
    return screenshot_path

# Re-run tests
pytest

# Check directory
dir reports\screenshots\

---

## Advanced Topics

### Q: How do I add a new test marker?

**A:**
   ini
# In pytest.ini, add to markers section:
markers =
    smoke: small set of critical tests
    my_new_marker: description of marker

# Then use in test:
@pytest.mark.my_new_marker
def test_something():
    pass

# Run:
pytest -m my_new_marker
---

### Q: Can I create custom fixtures?

**A:** Yes, in conftest.py:

   python
import pytest

@pytest.fixture(scope="function")
def my_fixture():
    """Fixture that runs before each test"""
    # Setup
    print("Setting up...")
    resource = "my resource"
    
    yield resource
    
    # Teardown
    print("Cleaning up...")

# Use in test
def test_with_fixture(my_fixture):
    print(my_fixture)  # "my resource"
    assert True
---

### Q: How do I run tests on different environments?

**A:**
   powershell
# Edit config.yaml
# env: qa  → Use QA
# env: prod → Use Production

# Or set via environment variable (advanced)
$env:TEST_ENV="prod"

# In code:
import os
env = os.getenv("TEST_ENV", "qa")

---

### Q: Can I integrate with CI/CD?

**A:** Yes! Example GitHub Actions:

   yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: pytest

---

### Q: Can I create test data fixtures?

**A:** Yes:

   python
# conftest.py
@pytest.fixture
def test_project_data():
    return {
        "name": "Test Project",
        "id": "123",
        "databases": ["DB1", "DB2"]
    }

# Use in test
def test_create_project(authenticated_page, test_project_data):
    project = test_project_data
    # Use project data in test

---

### Q: How do I measure test performance?

**A:**
   powershell
# Show slowest 10 tests
pytest --durations=10

# Output shows test duration
# test_home.py::test_home_page_load 5.23s
# test_ap.py::test_create_ap 4.12s
# ...

# Profile specific test
pytest tests/slow_test.py -v --durations=0

---

### Q: Can I mock API calls?

**A:** Yes, but Playwright automates browser, not API calling:

   python
# To mock API, intercept network:
page.route("**/api/data", lambda route: route.abort())

# Or mock response:
def handle_route(route):
    route.abort() if route.request.resource_type == "image" else route.continue_()

page.route("**/*", handle_route)

---

### Q: How do I add custom reporting?

**A:** Use Allure annotations:

   python
import allure

@allure.feature("Home Page")
@allure.story("Project Search")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_project(authenticated_page):
    """Description of test"""
    pass

# Annotations add metadata visible in Allure report

---

## Still Stuck?

### Try These Resources (in order):

1. **This FAQ** - You're reading it!
2. **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** - Common commands
3. **[README.md](./README.md)** - Full framework docs
4. **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Detailed setup steps
5. **Log files** - `reports/logs/execution.log`
6. **Screenshots** - `reports/screenshots/`
7. **Allure report** - `allure serve reports/allure-results`

### Ask for Help With:

- Test log output (copy-paste exact error)
- Screenshot showing the issue
- Exact command you ran
- Expected vs. actual result
- Steps to reproduce

---

## Emergency Checklist

When things go wrong:

- [ ] Reread the error message carefully
- [ ] Check test log: `Get-Content reports\logs\execution.log`
- [ ] Check screenshots: `start reports\screenshots\`
- [ ] Check config.yaml for correct environment
- [ ] Verify virtual environment is activated
- [ ] Try running single test in isolation
- [ ] Clear browser profile: `Remove-Item edge_profile -Recurse -Force`
- [ ] Regenerate auth: `python ../auth/save_login_state.py`
- [ ] Update dependencies: `pip install -r requirements.txt --upgrade`
- [ ] Restart terminal (fresh environment)

---

## Common Success Indicators

**You'll know it's working when**:
- Terminal shows `(venv)` at start
- `pytest` runs without module errors
- Browser opens automatically
- Tests complete and show PASSED/FAILED
- reports/report.html` opens in browser
- Screenshots in `reports/screenshots/
---

**Last Updated**: March 18, 2026  
**FAQ Version**: 1.0
