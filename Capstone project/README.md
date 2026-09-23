# Capstone Assignment 2: Selenium Python Automation Framework

A robust, enterprise-grade **Selenium Python Automation Testing Framework** built with **Page Object Model (POM)** architecture, supporting both **PyTest** and **Unittest** test runners.

---

## 🎯 Project Objective
Automate the **Login** and **Product Search** functionalities of an E-Commerce application ([TutorialsNinja](https://tutorialsninja.com/demo/)) using a scalable, maintainable, and modular test automation framework.

---

## 🏗️ Framework Architecture

```
capstone/
├── configurations/
│   ├── config.ini             # Application URLs, browser config, timeouts, credentials
│   └── config_reader.py       # Configuration parser utility
├── pages/                     # Page Object Model (POM) Layer
│   ├── __init__.py
│   ├── base_page.py           # Core Selenium wrapper (waits, clicks, typing, screenshots)
│   ├── home_page.py           # Navigation, header search, account dropdown
│   ├── login_page.py          # Credentials entry, submission, alert banners
│   ├── account_page.py        # Post-login verification, heading, logout
│   └── search_page.py         # Search results, product cards, no-match banner
├── test_data/                 # Test Data Files (Data-Driven Testing)
│   ├── login_data.csv         # Valid & invalid credentials for DDT
│   └── search_data.csv        # Valid & invalid search terms for DDT
├── utilities/                 # Framework Utilities
│   ├── __init__.py
│   ├── driver_factory.py      # Cross-browser initialization (Chrome, Firefox, Edge)
│   ├── csv_reader.py          # CSV parser for data-driven parameterization
│   ├── custom_logger.py       # Rotating logger (console & automation.log)
│   └── screenshot_util.py     # Captures and saves timestamped screenshots
├── tests/                     # Test Suites & Fixtures
│   ├── __init__.py
│   ├── conftest.py            # Pytest fixtures, CLI options, failure screenshot hook
│   ├── test_login_pytest.py   # Pytest: Single & DDT Login test cases
│   ├── test_search_pytest.py  # Pytest: Single & DDT Search test cases
│   ├── test_login_unittest.py # Unittest: Login test suite
│   ├── test_search_unittest.py# Unittest: Product Search test suite
│   └── run_unittest_suite.py  # Standalone Unittest suite runner
├── reports/                   # Execution Reports & Artifacts
│   ├── screenshots/           # Failure & verification screenshots
│   └── html_reports/          # pytest-html rich reports
├── logs/                      # Log files (automation.log)
├── pytest.ini                 # Pytest configuration, CLI options, and markers
├── requirements.txt           # Python package dependencies
└── README.md                  # Framework documentation
```

---

## ✨ Key Framework Features

| Feature | Description |
| :--- | :--- |
| **Page Object Model (POM)** | Strict separation of page locators/interactions from test validation logic. |
| **Dual Runner Support** | Full support for running tests via **PyTest** and Python's built-in **Unittest**. |
| **Data-Driven Testing (CSV)** | Automated parameterization loading test sets from CSV files (`login_data.csv`, `search_data.csv`). |
| **Configuration Management** | Centralized INI configuration (`config.ini`) for environments, browsers, timeouts, and paths. |
| **Screenshots on Failure** | Automatic capture of screenshots upon test failure, embedded directly in HTML reports and stored on disk. |
| **Rich HTML Reports** | Comprehensive `pytest-html` reports with execution duration, system metadata, and visual failure evidence. |
| **Cross-Browser Testing** | Easily switch between Chrome, Firefox, and Edge with optional headless execution. |
| **Robust Synchronization** | Centralized explicit waits (`WebDriverWait` + `expected_conditions`) in `BasePage` eliminating flaky sleep statements. |
| **Logging System** | Formatted dual-output logging (console + `logs/automation.log`) with timestamps, log levels, and source lines. |

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.9+ installed
- Google Chrome (or Firefox/Edge) installed

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration Management (`configurations/config.ini`)

You can customize browser settings, timeouts, and execution modes in `configurations/config.ini`:
```ini
[common]
base_url = https://tutorialsninja.com/demo/

[browser]
browser_name = chrome
headless = false
window_width = 1920
window_height = 1080

[timeouts]
implicit_wait = 10
explicit_wait = 15
page_load_timeout = 30
```

---

## 🧪 Running the Tests

### Option A: PyTest Test Runner

#### 1. Run all PyTest tests and generate HTML report:
```bash
pytest
```
*(Options like `--html=reports/html_reports/pytest_report.html --self-contained-html` are pre-configured in `pytest.ini`)*

#### 2. Run Headless mode via CLI:
```bash
pytest --headless=true
```

#### 3. Run specific browser:
```bash
pytest --browser=chrome
pytest --browser=firefox
pytest --browser=edge
```

#### 4. Run tests by Marker:
```bash
# Run Smoke tests only
pytest -m smoke

# Run Regression tests only
pytest -m regression

# Run Login tests only
pytest -m login

# Run Search tests only
pytest -m search

# Run Data-Driven tests only
pytest -m datadriven
```

---

### Option B: Unittest Test Runner

#### 1. Run via Custom Unittest Suite Runner:
```bash
python tests/run_unittest_suite.py
```

#### 2. Run via standard Unittest Discovery:
```bash
python -m unittest discover -s tests -p "test_*_unittest.py"
```

#### 3. Run a specific Unittest module:
```bash
python -m unittest tests/test_login_unittest.py
python -m unittest tests/test_search_unittest.py
```

---

## 📊 Reports and Artifacts

1. **HTML Report**: Located at `reports/html_reports/pytest_report.html`.
   - Open this file in any web browser to view detailed test statistics, pass/fail status, and embedded screenshots.
2. **Screenshots**: Any test failure automatically triggers a screenshot saved in `reports/screenshots/`.
3. **Logs**: Detailed execution trails are saved to `logs/automation.log`.

---

## 📝 Test Scenarios Automated

### 1. Login Functionality
- `TC_LOGIN_01`: Valid Login — Verifies successful authentication and redirection to `My Account` page.
- `TC_LOGIN_02`: Invalid Credentials — Verifies warning banner `Warning: No match for E-Mail Address and/or Password.`.
- `TC_LOGIN_03`: Empty Credentials — Verifies error banner when submitting empty fields.
- `TC_LOGIN_DDT`: Data-Driven Login — Validates multiple credential combinations from `test_data/login_data.csv`.

### 2. Product Search Functionality
- `TC_SEARCH_01`: Search Existing Product — Searches for "MacBook" and verifies product cards appear.
- `TC_SEARCH_02`: Search Non-Existing Product — Searches for "NonExistingLaptop999XYZ" and verifies no-match message.
- `TC_SEARCH_03`: Search Empty Query — Submits empty query and verifies criteria message.
- `TC_SEARCH_DDT`: Data-Driven Search — Validates search queries from `test_data/search_data.csv`.
