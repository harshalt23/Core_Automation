# Core Automation - Detailed Setup Guide

This guide provides step-by-step instructions for setting up the Core Automation Framework from scratch.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Pre-Setup Verification](#pre-setup-verification)
3. [Step-by-Step Installation](#step-by-step-installation)
4. [First Test Run](#first-test-run)
5. [Advanced Setup](#advanced-setup)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11 (64-bit)
- **Disk Space**: 2GB free (for dependencies, browsers, and reports)
- **RAM**: 4GB minimum (8GB recommended)
- **Internet**: Required for dependencies and initial setup

### Software to Install
- Python 3.9 or higher
- Microsoft Edge browser
- Git (optional, for version control)

---

## Pre-Setup Verification

### Check Python Installation

Open PowerShell and run:

```powershell
python --version
# Expected output: Python 3.9.x or higher

# Check if pip is available
pip --version
# Expected output: pip 21.x or higher
```

**If Python is not installed**:
1. Download from https://www.python.org/downloads/
2. Run installer
3. Check "Add Python to PATH"
4. Check "Install pip"
5. Click "Install Now"
6. Verify with `python --version` in new PowerShell window

---

### Check Edge Browser Installation

```powershell
# This command verifies Edge is installed
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe" | Select-Object "(Default)"

# Expected: Path to msedge.exe
```

**If Edge is not installed**:
1. Download from https://www.microsoft.com/en-us/edge
2. Run installer and follow prompts
3. Verify by opening Edge manually

---

## Step-by-Step Installation

### Step 1: Navigate to Project Directory

```powershell
# Navigate to your workspace
cd C:\Users\<YourUsername>\Core_Automation

# Verify you can see the project files
Get-ChildItem
# Should show: Core_Automation, auth, storage_state.json folders
```

### Step 2: Create Virtual Environment

A virtual environment ensures project dependencies don't conflict with system Python.

```powershell
# Create virtual environment named "venv"
python -m venv venv

# Verify it was created
Test-Path .\venv
# Expected output: True
```

### Step 3: Activate Virtual Environment

```powershell
# Activate the virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# You should see (venv) at the start of your terminal line
# Example: (venv) PS C:\Users\...\Core_Automation>

# If you get execution policy error:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try again
```

**To deactivate later**:
```powershell
deactivate
```

### Step 4: Upgrade pip

```powershell
# Ensure pip is the latest version
python -m pip install --upgrade pip

# Verify pip is up to date
pip --version
# Should show latest version
```

### Step 5: Install Dependencies

```powershell
# Install all required Python packages from requirements.txt
pip install -r requirements.txt

# This will install:
# - playwright (Web automation)
# - pytest (Testing framework)
# - pytest-playwright (Pytest plugin for Playwright)
# - pytest-xdist (Parallel test execution)
# - pytest-html (HTML reports)
# - allure-pytest (Allure reporting)
# - anthropic (Claude API)
# - And many more...

# Verify installation
pip list
# Should show all packages listed in requirements.txt
```

### Step 6: Install Playwright Browsers

Playwright needs to download browser binaries (Chromium, Firefox, WebKit):

```powershell
# Download browser binaries
playwright install

# This downloads:
# - Chromium
# - Firefox
# - WebKit
# - Webkit (used for testing)

# For Edge only (faster if you only use Edge):
# playwright install msedge
```

**Note**: First run may take 5-10 minutes depending on internet speed.

### Step 7: Set Up Authentication

Navigate to the Core_Automation directory and authenticate:

```powershell
# Go to Core_Automation subdirectory
cd Core_Automation

# Run the login script
python ..\auth\save_login_state.py

# A browser window will open automatically
```

**Follow these steps**:
1. **Browser opens** → Core application login page
2. **Login manually**:
   - Look for login form or SSO option
   - Enter credentials if direct login
   - Or complete Microsoft Authenticator flow
3. **Complete MFA** (if required):
   - Approve on your phone
   - Wait for redirect to Core dashboard
4. **Return to PowerShell**:
   - Once you see the Core dashboard in browser
   - Press **ENTER** in the PowerShell terminal
5. **Verify storage**:
   - Check `auth\storage_states\admin.json` was created

**Troubleshooting - Manual Login**:
```powershell
# If automatic browser doesn't open:
python ..\auth\save_login_state.py

# When prompted, paste this in your browser:
# https://core-dev.mma.com/core_v2/ui/

# Then complete login steps manually
```

### Step 8: Verify Installation

Run a quick smoke test to ensure everything works:

```powershell
# Back in Core_Automation directory
cd C:\Users\<YourUsername>\Core_Automation\Core_Automation

# Run a quick test
pytest tests\sanity\test_basic_launch.py -v

# Expected output:
# test_basic_launch.py PASSED
```

---

## First Test Run

### Run Your First Test

```powershell
# Make sure you're in the Core_Automation/Core_Automation directory
# And virtual environment is activated (you see (venv) in terminal)

# Run home page tests
pytest tests\home\test_home.py -v

# Expected output:
# test_home_page_load PASSED
# test_expand_project_from_home PASSED
```

### View Test Reports

After tests complete:

```powershell
# View HTML report
start reports\report.html

# View screenshots of any failures
start reports\screenshots\

# View execution logs
Get-Content reports\logs\execution.log -Tail 50

# View Allure report (requires Java)
# First check if Java is installed
java -version

# If Java installed, run:
allure serve reports\allure-results
```

### Run Multiple Tests with Markers

```powershell
# All smoke tests
pytest -m smoke -v

# All regression tests
pytest -m regression -v

# Specific module tests
pytest -m module_home -v

# Combine markers (OR logic)
pytest -m "smoke or module_home" -v
```

---

## Advanced Setup

### Configure IDE Integration

#### Visual Studio Code Setup

1. **Install Python Extension**:
   - Open VS Code
   - Extensions → Python (by Microsoft)
   - Click Install

2. **Select Python Interpreter**:
   - Ctrl + Shift + P
   - Type: "Python: Select Interpreter"
   - Choose the one in: `.\venv\Scripts\python.exe`

3. **Run Tests from IDE**:
   - Install Pytest extension
   - Click test icon on left sidebar
   - Tests auto-discover and can run individually

#### PyCharm Setup

1. **Open Project**:
   - File → Open
   - Select Core_Automation folder

2. **Configure Interpreter**:
   - File → Settings → Project → Python Interpreter
   - Click gear icon → Add
   - Choose "Existing environment"
   - Browse to: `C:\...\Core_Automation\venv\Scripts\python.exe`
   - Click OK

3. **Run Tests**:
   - Right-click test file
   - Select "Run pytest in ..."

### Enable CI/CD Integration

Create `.github/workflows/tests.yml` for GitHub Actions:

```yaml
name: Core Automation Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        playwright install

    - name: Run tests
      run: pytest tests/ -v
```

Commit this file to enable automated testing on push.

### Parallel Test Execution

Run multiple tests simultaneously to save time:

```powershell
# Run with 4 parallel workers
pytest -n 4

# Auto-detect CPU count
pytest -n auto

# Distribute by test scope (safer for shared resources)
pytest -n 4 --dist loadscope
```

### Generate Allure Reports

Requires Java to be installed. If not installed, skip this section.

```powershell
# Run tests with Allure reporting
pytest --alluredir=reports\allure-results

# Generate and serve Allure report
allure serve reports\allure-results

# Report opens in browser automatically
# View detailed test histories, trends, failures
```

---

## Troubleshooting

### Installation Issues

#### Error: "No module named 'pip'"

```powershell
# Reinstall pip
python -m ensurepip --upgrade

# Try installing again
pip install -r requirements.txt
```

#### Error: "python: command not found"

Your Python PATH isn't set. Options:

**Option 1**: Use full path
```powershell
C:\Python311\python.exe -m venv venv
```

**Option 2**: Reinstall Python with PATH
- Uninstall Python
- Reinstall, making sure to check "Add Python to PATH"

#### Error: "ExecutionPolicy" in PowerShell

```powershell
# Allow scripts to run
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run activation again
.\venv\Scripts\Activate.ps1
```

### Playwright Issues

#### Error: "playwright: command not found"

```powershell
# Make sure venv is activated (you see (venv) in terminal)

# Reinstall playwright
pip uninstall playwright
pip install playwright

# Install browsers
playwright install
```

#### Error: "Timeout waiting for browser launch"

```powershell
# Browser might not exist. Install it:
playwright install

# Or install Edge only:
playwright install msedge

# If still fails, check Edge is actually installed
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe"
```

#### Error: "Channel 'msedge' is not installed"

```powershell
# Reinstall Playwright with Edge
playwright install

# Or if Edge isn't installed, install it:
# Download from https://www.microsoft.com/en-us/edge
```

### Test Execution Issues

#### Error: "FAILED - ModuleNotFoundError: No module named 'modules'"

```powershell
# Make sure you're in correct directory:
cd Core_Automation\Core_Automation

# Then run tests:
pytest tests\ -v
```

#### Error: "Cannot find auth storage (admin.json)"

```powershell
# Regenerate authentication:
cd ..\auth
python save_login_state.py

# Follow login prompts, then press ENTER to save

# Verify file was created:
Test-Path storage_states\admin.json
```

#### Error: "TimeoutError: Timeout exceeded"

Common causes and solutions:

```powershell
# 1. Application might be slow - increase timeout in config.yaml:
# timeouts:
#   action_timeout: 30000  # Increase from 20000

# 2. View what happened with screenshots:
start reports\screenshots\

# 3. Check logs:
Get-Content reports\logs\execution.log

# 4. Re-run single test with verbose output:
pytest tests\home\test_home.py::test_home_page_load -v -s
```

#### Error: "Channel is not registered"

```powershell
# Edge not fully installed. Try:
playwright install msedge

# Or uninstall and reinstall Playwright:
pip uninstall -y playwright
pip install playwright
playwright install msedge
```

### Virtual Environment Issues

#### Lost Virtual Environment

```powershell
# If venv is corrupted, recreate it:

# Delete old one
Remove-Item -Recurse -Force venv

# Create new one
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
playwright install
```

#### Deactivate (leave virtual environment)

```powershell
# When done working on this project
deactivate

# Or close PowerShell and open new window
```

### Report Generation Issues

#### No reports generated

```powershell
# Make sure report directories exist:
mkdir reports\screenshots
mkdir reports\traces
mkdir reports\logs
mkdir reports\allure-results

# Then run tests again:
pytest tests\ -v
```

#### Allure reports show "No test results"

```powershell
# Java might not be installed check:
java -version

# If not found, download from https://www.java.com

# Or generate static report (no Java needed):
allure generate reports\allure-results -o allure-report
start allure-report\index.html
```

---

## Next Steps

After successful setup:

1.  Read the main [README.md](./README.md) for framework overview
2.  Learn test structure in [Writing Tests](./README.md#writing-tests) section
3.  Review [Best Practices](./README.md#best-practices)
4.  Start writing tests for new features
5.  Set up CI/CD pipeline if needed

---

## Additional Resources

- **Playwright Official Docs**: https://playwright.dev/python/
- **pytest Documentation**: https://docs.pytest.org/
- **Python Virtual Environments**: https://docs.python.org/3/tutorial/venv.html
- **Microsoft Edge Download**: https://www.microsoft.com/en-us/edge

---

## Need Help?

1. Check this guide first
2. Review main README.md [Troubleshooting](./README.md#troubleshooting) section
3. Check logs: `reports/logs/execution.log`
4. Run tests with verbose output: `pytest -v -s`

---

**Last Updated**: March 18, 2026  
**Maintained By**: Automation Team
