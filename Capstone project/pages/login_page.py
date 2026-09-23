from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.account_page import AccountPage

class LoginPage(BasePage):
    """Page Object for TutorialsNinja Login Page."""

    # Locators
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.XPATH, "//input[@value='Login']")
    FORGOTTEN_PASSWORD_LINK = (By.LINK_TEXT, "Forgotten Password")
    ALERT_WARNING = (By.CSS_SELECTOR, ".alert-danger")
    RETURNING_CUSTOMER_HEADING = (By.XPATH, "//h2[text()='Returning Customer']")
    NEW_CUSTOMER_HEADING = (By.XPATH, "//h2[text()='New Customer']")

    def __init__(self, driver):
        super().__init__(driver)

    def is_login_page_displayed(self):
        """Verifies if login elements are present on the page."""
        return self.is_element_displayed(self.EMAIL_INPUT) and self.is_element_displayed(self.LOGIN_BUTTON)

    def enter_email(self, email):
        """Enters the provided email address into the email input field."""
        self.send_keys(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        """Enters the provided password into the password input field."""
        self.send_keys(self.PASSWORD_INPUT, password)

    def click_login_button(self):
        """Clicks on the Login submit button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, email, password):
        """Performs full login sequence and returns AccountPage instance."""
        self.logger.info(f"Submitting login credentials for email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return AccountPage(self.driver)

    def get_alert_warning_message(self):
        """Retrieves warning banner text on invalid or failed login."""
        return self.get_text(self.ALERT_WARNING)

    def is_alert_warning_displayed(self):
        """Checks whether error/warning banner is displayed."""
        return self.is_element_displayed(self.ALERT_WARNING, timeout=6)
