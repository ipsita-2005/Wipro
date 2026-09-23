import os
import base64
import pytest
from datetime import datetime
from configurations.config_reader import ConfigReader
from utilities.driver_factory import DriverFactory
from utilities.screenshot_util import ScreenshotUtil
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("Conftest")

def pytest_addoption(parser):
    """Adds custom command-line options for pytest execution."""
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Browser type: chrome, firefox, or edge"
    )
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="Run browser in headless mode: true or false"
    )

@pytest.fixture(scope="function")
def driver(request):
    """Pytest fixture to initialize and tear down WebDriver per test function."""
    browser_cli = request.config.getoption("--browser")
    headless_cli = request.config.getoption("--headless")

    browser = browser_cli if browser_cli else ConfigReader.get_browser_name()
    if headless_cli is not None:
        headless = headless_cli.lower() in ("true", "1", "yes")
    else:
        headless = ConfigReader.get_headless()

    logger.info(f"Setting up WebDriver fixture (Browser={browser}, Headless={headless})")
    driver_instance = DriverFactory.get_driver(browser_name=browser, headless=headless)
    
    # Store driver on request.node for hooks (such as screenshot makereport)
    request.node.driver = driver_instance

    base_url = ConfigReader.get_base_url()
    logger.info(f"Opening base URL: {base_url}")
    driver_instance.get(base_url)

    yield driver_instance

    logger.info("Tearing down WebDriver fixture")
    try:
        driver_instance.quit()
    except Exception as e:
        logger.warning(f"Error while quitting WebDriver: {e}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture screenshots upon test failure and attach them to HTML report."""
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        # Check if test failed or unexpected pass
        if (report.failed and not xfail) or (report.passed and xfail):
            driver_instance = getattr(item, "driver", None)
            if not driver_instance:
                # Attempt to get from funcargs
                driver_instance = item.funcargs.get("driver", None)

            if driver_instance:
                screenshot_path = ScreenshotUtil.capture_screenshot(driver_instance, item.name)
                if screenshot_path and os.path.exists(screenshot_path):
                    try:
                        with open(screenshot_path, "rb") as img_file:
                            encoded_bytes = base64.b64encode(img_file.read()).decode("utf-8")
                        html_snippet = (
                            f'<div><p style="margin: 4px 0; font-weight: bold; color: #d9534f;">Failure Screenshot:</p>'
                            f'<a href="data:image/png;base64,{encoded_bytes}" target="_blank">'
                            f'<img src="data:image/png;base64,{encoded_bytes}" alt="Failure Screenshot" '
                            f'style="max-width:480px; max-height:270px; border: 2px solid #d9534f; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);"/>'
                            f'</a></div>'
                        )
                        import pytest_html
                        extras.append(pytest_html.extras.html(html_snippet))
                        logger.info(f"Embedded failure screenshot for test '{item.name}' into report.")
                    except Exception as err:
                        logger.error(f"Error embedding screenshot into HTML report: {err}")

        report.extras = extras

def pytest_html_report_title(report):
    """Sets a customized title for the generated pytest-html report."""
    report.title = "Capstone 2: TutorialsNinja Automation Test Report"

def pytest_configure(config):
    """Customizes pytest environment metadata in HTML report."""
    if hasattr(config, "_metadata"):
        config._metadata["Project"] = "Capstone Assignment 2 - E-Commerce Automation"
        config._metadata["Application Under Test"] = ConfigReader.get_base_url()
        config._metadata["Framework"] = "Selenium Python + PyTest + Unittest + POM"
        config._metadata["Author"] = "QA Automation Engineer"
        config._metadata["Execution Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
