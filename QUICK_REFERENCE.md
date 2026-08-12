# Core Automation - Quick Reference Guide

A quick lookup guide for common commands and workflows in the Core Automation Framework.

## Quick Start (First Time)

```powershell
# 1. Navigate to project
cd C:\Users\<YourUsername>\Core_Automation

# 2. Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
playwright install

# 4. Setup authentication
cd Core_Automation
python ..\auth\save_login_state.py
# [Login manually when browser opens, then press ENTER]

# 5. Run first test
cd C:\Users\<YourUsername>\Core_Automation\Core_Automation
pytest tests\sanity\test_basic_launch.py -v

# 6. View results
start reports\report.html
```

---

## Common Commands

### Running Tests

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -s` | Show print statements |
| `pytest -x` | Stop on first failure |
| `pytest -m smoke` | Run smoke tests only |
| `pytest -m regression` | Run all regression tests |
| `pytest -m module_ap` | Run Analytical Plan tests |
| `pytest tests/home/test_home.py` | Single test file |
| `pytest tests/home/test_home.py::test_home_page_load` | Single test |
| `pytest -k "home"` | Tests matching pattern |
| `pytest -n auto` | Parallel execution |
| `pytest -n 4` | Run with 4 workers |
| `pytest --lf` | Run last failed tests |
| `pytest --ff` | Failed first, then others |
| `pytest --reruns 2` | Retry failed tests 2x |
| `pytest --durations=5` | Show 5 slowest tests |

### Viewing Reports

| Command | Purpose |
|---------|---------|
| `start reports\report.html` | HTML report |
| `allure serve reports\allure-results` | Allure dashboard (requires Java) |
| `start reports\screenshots\` | Screenshot folder |
| `start reports\traces\` | Trace recordings |
| `Get-Content reports\logs\execution.log -Tail 50` | Last 50 lines of log |

### Environment Setup

| Command | Purpose |
|---------|---------|
| `.\venv\Scripts\Activate.ps1` | Activate  virtual environment |
| `deactivate` | Deactivate virtual environment |
| `pip list` | Show installed packages |
| `pip install -r requirements.txt` | Install dependencies |
| `playwright install` | Install browser binaries |
| `python ..\auth\save_login_state.py` | Re-generate auth token |

### Configuration

| Command | Purpose |
|---------|---------|
| Edit `config/config.yaml` | Change environment/env settings |
| Set `env: qa` | Use QA environment |
| Set `env: prod` | Use Production environment |
| Set `headless: true` | Run without UI |
| Set `headless: false` | Show browser UI |

---

## Test Markers

Add `@pytest.mark.<marker>` to your tests:

```python
@pytest.mark.smoke           # Quick sanity test
@pytest.mark.regression      # Full regression test
@pytest.mark.module_ap       # Analytical Plan module
@pytest.mark.module_wb       # Workbook module
@pytest.mark.module_ads      # Analytic Dataset
@pytest.mark.module_mm       # Main Model
@pytest.mark.module_ps       # Project Specs
@pytest.mark.module_ai       # Activate Input
@pytest.mark.module_home     # Home page
@pytest.mark.e2e            # End-to-end test
```

---

## File Locations Quick Map

```
Key Files:
├── config.yaml              → config/config.yaml
├── Test runner config       → pytest.ini
├── Fixtures                 → conftest.py
├── Main documentation       → README.md
├── Setup guide             → SETUP_GUIDE.md
├── Contributing            → CONTRIBUTING.md
├── Architecture            → PROJECT_STRUCTURE.md
│
Test Files:
├── Home tests              → tests/home/test_home.py
├── Analytical Plan tests   → tests/analytical_plan/test_analytical_plan.py
├── Sanity tests            → tests/sanity/test_basic_launch.py
│
Page Objects:
├── Home page               → modules/home/pages/home.py
├── Analytical Plan page    → modules/analytical_plan/pages/analytical_plan.py
├── Locators                → modules/*/pages/*_locator.py
│
Utilities:
├── Config reader           → utils/config_reader.py
├── Logger setup            → utils/logger_utils.py
├── Auth helper             → utils/auth.py
├── Base page               → utils/base_page.py
│
Reports (auto-generated):
├── HTML report             → reports/report.html
├── Allure data             → reports/allure-results/
├── Screenshots             → reports/screenshots/
├── Traces                  → reports/traces/
├── Logs                    → reports/logs/execution.log
```

---

## Common Workflows

### Adding a New Test

```powershell
# 1. Create test file
# tests/my_module/test_my_feature.py

# 2. Write test
@pytest.mark.smoke
def test_my_feature(authenticated_page):
    page = MyFeaturePage(authenticated_page)
    page.perform_action()
    assert expected_result

# 3. Run test
pytest tests/my_module/test_my_feature.py -v

# 4. View results
start reports/report.html
```

### Creating New Page Object

```powershell
# 1. Create locator file
# modules/my_feature/pages/my_feature_locator.py
class MyFeatureLocator:
    def __init__(self, page):
        self.my_button = page.get_by_text("Click")

# 2. Create page file
# modules/my_feature/pages/my_feature.py
class MyFeaturePage:
    def __init__(self, page):
        self.locator = MyFeatureLocator(page)
    
    def click_button(self):
        self.locator.my_button.click()

# 3. Use in test
from modules.my_feature.pages.my_feature import MyFeaturePage

def test_my_feature(authenticated_page):
    page = MyFeaturePage(authenticated_page)
    page.click_button()
```

### Debugging a Failed Test

```powershell
# 1. Check screenshots
start reports/screenshots/

# 2. View logs
Get-Content reports/logs/execution.log -Tail 100

# 3. Run with verbose output
pytest tests/failing_test.py -v -s

# 4. Run with Allure trace
pytest tests/failing_test.py --alluredir=reports/allure-results
allure serve reports/allure-results

# 5. Increase timeout in config.yaml
# timeouts:
#   action_timeout: 30000

# 6. Re-run test
pytest tests/failing_test.py -v
```

### Fixing a Flaky Test

```powershell
# 1. Identify the flaky test
# Example: test_search_returns_results

# 2. Add retry logic
pytest --reruns 3 tests/failing_test.py

# 3. Fix root cause (usually hard waits)
# BAD: page.wait_for_timeout(5000)
# GOOD: element.wait_for(state="visible")

# 4. Verify fix
pytest tests/failing_test.py -v --reruns 2
```

### Switching Environments

```powershell
# Edit config/config.yaml
env: qa              # Change to qa

# Or
env: prod            # Change to prod

# Run tests
pytest tests/ -m smoke

# Verify correct environment
pytest tests/sanity/test_basic_launch.py -v -s
# Should print: Base URL: https://core-dev.mma.com/... (for QA)
```

### Running Tests in Parallel

```powershell
# Auto-detect CPU count
pytest -n auto

# Specific workers
pytest -n 4

# Parallel by test scope (recommended for shared resources)
pytest -n 4 --dist loadscope

# Check progress
# Terminal shows: [gw0] [gw1] [gw2] [gw3] (4 workers)
```

### Generating Reports

```powershell
# HTML Report (always generated)
pytest
start reports/report.html

# Allure Report (requires Java)
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
# Automatically opens in browser

# Output summary
pytest -v
# Shows PASSED/FAILED count at end
```

---

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Tests fail with timeout | Increase timeout in config.yaml |
| "Module not found" error | Navigate to Core_Automation/Core_Automation folder |
| Virtual env not activated | Run `.\venv\Scripts\Activate.ps1` |
| Playwright not found | Run `pip install playwright` then `playwright install` |
| Browser won't launch | Run `playwright install msedge` |
| Auth failed | Run `python ../auth/save_login_state.py` again |
| parallel tests lock | Remove: `Remove-Item edge_profile_gw* -Recurse -Force` |
| No reports generated | Create folders: `mkdir reports/screenshots` etc. |
| Allure won't serve | Install Java from java.com |

---

## IDE Integration

### Visual Studio Code

```powershell
# 1. Install Python extension (Microsoft)
# 2. Select interpreter: Ctrl+Shift+P → "Python: Select Interpreter"
# 3. Choose: .\venv\Scripts\python.exe
# 4. Install Pytest extension
# 5. Click test icon (flask) on sidebar
# 6. Tests auto-discover and show as tree
# 7. Click run button next to test to execute
```

### PyCharm

```
1. File → Open → Select Core_Automation folder
2. File → Settings → Project → Python Interpreter
3. Click gear → Add → Existing environment
4. Browse to: C:\...\Core_Automation\venv\Scripts\python.exe
5. Right-click test file → Run pytest...
6. Tests show in "Run" tab at bottom
```

---

## Git Workflow

```powershell
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add new test for feature X"

# Push to fork
git push origin feature/my-feature

# Create Pull Request on GitHub
# [GitHub UI] → Compare & pull request

# After review, merge to main
# [GitHub UI] → Merge pull request
```

---

## Configuration Quick Reference

### config.yaml Timeouts

```yaml
page_load: 90000      # 90 seconds (page.goto)
action_timeout: 20000 # 20 seconds (element.click, fill, etc)

# Increase timeouts for:
# - Slow environments
# - Complex pages
# - MFA/authentication delay
```

### pytest.ini Markers

```ini
markers =
    smoke: quick sanity tests
    regression: full suite
    module_ap: analytical plan tests
    # Add custom markers here
```

### Browser Options

```yaml
browser: chromium      # chromium, firefox, webkit
headless: false        # true for CI, false for debugging
```

---

## Useful Links

| Resource | URL |
|----------|-----|
| Playwright Docs | https://playwright.dev/python/ |
| Pytest Docs | https://docs.pytest.org/ |
| Allure Docs | https://docs.qameta.io/allure/ |
| Python PEP 8 | https://pep8.org/ |
| Page Object Design | https://martinfowler.com/bliki/PageObject.html |

---

## Key Concepts

### Fixtures
Pre-configured resources provided to tests (e.g., browser)
```python
def test_my_test(authenticated_page):  # authenticated_page is fixture
    pass
```

### Markers
Labels for organizing and filtering tests
```python
@pytest.mark.smoke  # Run: pytest -m smoke
def test_something():
    pass
```

### Locators
CSS/XPath selectors for finding elements
```python
button = page.get_by_text("Click Me")
```

### Page Object
Class encapsulating page interactions
```python
page_obj = HomePage(page)
page_obj.click_button()
```

### Assertions
Validations that test passes
```python
assert "Expected" in page.content()
```

---

## Performance Tips

1. **Use specific waits**: `element.wait_for()` not `page.wait_for_timeout()`
2. **Run parallel**: `pytest -n auto` saves ~60% time
3. **Use markers**: `pytest -m smoke` for quick checks
4. **Cache login**: Persistent profiles avoid re-login
5. **Limit headless**: Set `headless: false` for debugging only

---

## Pro Tips

✨ **Tip 1**: Use `-s` flag to see print statements
```powershell
pytest -s  # Shows all print() output
```

✨ **Tip 2**: Stop on first failure
```powershell
pytest -x  # Stops immediately on failure
```

✨ **Tip 3**: Run previously failed tests
```powershell
pytest --lf  # Only runs tests that failed last time
```

✨ **Tip 4**: Show slowest tests
```powershell
pytest --durations=10  # Shows 10 slowest tests
```

✨ **Tip 5**: Combine markers
```powershell
pytest -m "smoke and module_ap"  # AND logic
pytest -m "smoke or regression"  # OR logic
```

---

## Emergency Commands

```powershell
# Complete cleanup (start fresh)
Remove-Item -Recurse -Force venv
Remove-Item -Recurse -Force reports
Remove-Item -Recurse -Force edge_profile*
python -m venv venv

# Reset and reinstall everything
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --force-reinstall
playwright install

# Clear all Python cache
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force .pytest_cache
```

---

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError` | Wrong directory | `cd Core_Automation/Core_Automation` |
| `TimeoutError` | Element not found | Check screenshot, increase timeout |
| `playwright not found` | Not installed | `pip install playwright` |
| `Channel 'msedge' not found` | Edge not installed | `playwright install msedge` |
| `Cannot find admin.json` | Auth not done | Run `python ../auth/save_login_state.py` |
| `No such file` | Wrong path | Check file location |

---

## Still Need Help?

1. **Check main README.md** - Full documentation
2. **Check SETUP_GUIDE.md** - Step-by-step setup
3. **Check PROJECT_STRUCTURE.md** - Architecture details
4. **Review CONTRIBUTING.md** - Best practices
5. **Check test logs** - `reports/logs/execution.log`
6. **View screenshots** - `start reports/screenshots/`
7. **Review conftest.py** - Fixture details

---

**Last Updated**: March 18, 2026  
**Quick Reference v1.0**
