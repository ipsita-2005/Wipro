import pytest
from pathlib import Path
from configurations.config_reader import ConfigReader
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from utilities.csv_reader import CSVReader
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("TestLoginPytest")

# Path to login test data
LOGIN_CSV_PATH = Path(__file__).resolve().parent.parent / "test_data" / "login_data.csv"
LOGIN_TEST_DATA = CSVReader.get_csv_rows_as_tuples(str(LOGIN_CSV_PATH))

class TestLoginPytest:
    """Test suite for Login functionality using PyTest and POM."""

    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, driver):
        """TC_LOGIN_01: Verify user can successfully log in with valid credentials."""
        logger.info("Executing test_valid_login")
        home_page = HomePage(driver)
        login_page = home_page.navigate_to_login_page()

        assert login_page.is_login_page_displayed(), "Login page elements were not displayed."

        valid_email, valid_password = ConfigReader.get_valid_credentials()
        account_page = login_page.login(valid_email, valid_password)

        assert account_page.is_account_heading_displayed(), "Account heading was not displayed after valid login."
        assert account_page.get_heading_text() == "My Account", f"Unexpected heading: {account_page.get_heading_text()}"
        
        # Teardown state by logging out
        account_page.logout()

    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_credentials_login(self, driver):
        """TC_LOGIN_02: Verify warning banner when logging in with invalid credentials."""
        logger.info("Executing test_invalid_credentials_login")
        home_page = HomePage(driver)
        login_page = home_page.navigate_to_login_page()

        login_page.login("non_existing_user_999@test.com", "WrongPassword123")
        assert login_page.is_alert_warning_displayed(), "Warning banner was not displayed on invalid login."

        warning_text = login_page.get_alert_warning_message()
        assert (
            "Warning: No match for E-Mail Address and/or Password." in warning_text or
            "exceeded allowed number of login attempts" in warning_text
        ), f"Unexpected warning text received: '{warning_text}'"

    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_credentials_login(self, driver):
        """TC_LOGIN_03: Verify warning banner when submitting empty login form."""
        logger.info("Executing test_empty_credentials_login")
        home_page = HomePage(driver)
        login_page = home_page.navigate_to_login_page()

        login_page.login("", "")
        assert login_page.is_alert_warning_displayed(), "Warning banner was not displayed on empty credentials."

        warning_text = login_page.get_alert_warning_message()
        assert (
            "Warning: No match for E-Mail Address and/or Password." in warning_text or
            "exceeded allowed number of login attempts" in warning_text
        ), f"Unexpected warning text received: '{warning_text}'"

    @pytest.mark.datadriven
    @pytest.mark.login
    @pytest.mark.parametrize("tc_id, email, password, expected_status, expected_message", LOGIN_TEST_DATA)
    def test_data_driven_login(self, driver, tc_id, email, password, expected_status, expected_message):
        """TC_LOGIN_DDT: Data-driven login test executing across all records in CSV."""
        logger.info(f"Executing {tc_id} with email: '{email}', expected: '{expected_status}'")
        home_page = HomePage(driver)
        login_page = home_page.navigate_to_login_page()

        if expected_status == "success":
            account_page = login_page.login(email, password)
            assert account_page.is_account_heading_displayed(), f"Failed to reach account page for {tc_id}"
            assert expected_message in account_page.get_heading_text()
            account_page.logout()
        else:
            login_page.login(email, password)
            assert login_page.is_alert_warning_displayed(), f"Warning banner missing for {tc_id}"
            actual_msg = login_page.get_alert_warning_message()
            assert (
                expected_message in actual_msg or
                "exceeded allowed number of login attempts" in actual_msg
            ), f"Message mismatch in {tc_id}. Received: '{actual_msg}'"
