import os
import sys
from pathlib import Path

# Add project root directory to sys.path for direct script execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import unittest
from configurations.config_reader import ConfigReader
from utilities.driver_factory import DriverFactory
from utilities.screenshot_util import ScreenshotUtil
from utilities.csv_reader import CSVReader
from utilities.custom_logger import CustomLogger
from pages.home_page import HomePage

logger = CustomLogger.get_logger("TestLoginUnittest")

LOGIN_CSV_PATH = Path(__file__).resolve().parent.parent / "test_data" / "login_data.csv"

class TestLoginUnittest(unittest.TestCase):
    """Unittest TestCase implementation for Login scenarios."""

    def setUp(self):
        """Initializes browser and navigates to the application before each test."""
        logger.info(f"--- Starting Unittest: {self._testMethodName} ---")
        self.driver = DriverFactory.get_driver()
        self.base_url = ConfigReader.get_base_url()
        self.driver.get(self.base_url)

    def tearDown(self):
        """Captures screenshot if test encountered failure, and terminates driver."""
        test_failed = False
        res = getattr(getattr(self, "_outcome", None), "result", None)
        if res:
            test_failed = any(test == self for test, _ in getattr(res, "failures", [])) or \
                          any(test == self for test, _ in getattr(res, "errors", []))

        if test_failed:
            logger.warning(f"Test {self._testMethodName} FAILED. Capturing screenshot...")
            ScreenshotUtil.capture_screenshot(self.driver, f"unittest_failure_{self._testMethodName}")

        logger.info(f"--- Ending Unittest: {self._testMethodName} ---")
        if self.driver:
            self.driver.quit()

    def test_valid_login(self):
        """TC_UNITTEST_LOGIN_01: Verify successful login with valid credentials."""
        home_page = HomePage(self.driver)
        login_page = home_page.navigate_to_login_page()
        self.assertTrue(login_page.is_login_page_displayed(), "Login page was not displayed.")

        valid_email, valid_password = ConfigReader.get_valid_credentials()
        account_page = login_page.login(valid_email, valid_password)

        self.assertTrue(account_page.is_account_heading_displayed(), "Account heading was not displayed.")
        self.assertEqual(account_page.get_heading_text(), "My Account", "Heading text mismatch.")
        account_page.logout()

    def test_invalid_credentials_login(self):
        """TC_UNITTEST_LOGIN_02: Verify warning banner upon invalid login attempt."""
        home_page = HomePage(self.driver)
        login_page = home_page.navigate_to_login_page()

        login_page.login("non_existent_999@test.com", "InvalidPass123")
        self.assertTrue(login_page.is_alert_warning_displayed(), "Warning banner not displayed.")
        warning_msg = login_page.get_alert_warning_message()
        self.assertTrue(
            "Warning: No match for E-Mail Address and/or Password." in warning_msg or
            "exceeded allowed number of login attempts" in warning_msg,
            f"Unexpected warning: '{warning_msg}'"
        )

    def test_empty_credentials_login(self):
        """TC_UNITTEST_LOGIN_03: Verify warning banner upon empty login fields."""
        home_page = HomePage(self.driver)
        login_page = home_page.navigate_to_login_page()

        login_page.login("", "")
        self.assertTrue(login_page.is_alert_warning_displayed(), "Warning banner not displayed on empty login.")
        warning_msg = login_page.get_alert_warning_message()
        self.assertTrue(
            "Warning: No match for E-Mail Address and/or Password." in warning_msg or
            "exceeded allowed number of login attempts" in warning_msg,
            f"Unexpected warning: '{warning_msg}'"
        )

    def test_data_driven_login_from_csv(self):
        """TC_UNITTEST_LOGIN_DDT: Executes all records from CSV using subTest."""
        records = CSVReader.get_csv_rows_as_tuples(str(LOGIN_CSV_PATH))
        for tc_id, email, password, expected_status, expected_message in records:
            with self.subTest(test_case_id=tc_id, email=email):
                logger.info(f"Running subtest {tc_id} for email: {email}")
                self.driver.get(self.base_url)
                home_page = HomePage(self.driver)
                login_page = home_page.navigate_to_login_page()

                if expected_status == "success":
                    account_page = login_page.login(email, password)
                    self.assertTrue(account_page.is_account_heading_displayed(), f"Failed to login in {tc_id}")
                    self.assertIn(expected_message, account_page.get_heading_text())
                    account_page.logout()
                else:
                    login_page.login(email, password)
                    self.assertTrue(login_page.is_alert_warning_displayed(), f"Warning missing in {tc_id}")
                    actual_msg = login_page.get_alert_warning_message()
                    self.assertTrue(
                        expected_message in actual_msg or "exceeded allowed number of login attempts" in actual_msg,
                        f"Unexpected warning message in {tc_id}: '{actual_msg}'"
                    )

if __name__ == "__main__":
    unittest.main()
