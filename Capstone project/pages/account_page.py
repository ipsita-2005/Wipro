from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class AccountPage(BasePage):
    """Page Object for the My Account page (after successful login)."""

    # Locators
    ACCOUNT_HEADING = (By.XPATH, "//div[@id='content']/h2[text()='My Account']")
    EDIT_ACCOUNT_LINK = (By.LINK_TEXT, "Edit your account information")
    PASSWORD_CHANGE_LINK = (By.LINK_TEXT, "Change your password")
    LOGOUT_LINK = (By.XPATH, "//aside[@id='column-right']//a[text()='Logout']")
    LOGOUT_HEADER = (By.XPATH, "//div[@id='content']/h1[text()='Account Logout']")

    def __init__(self, driver):
        super().__init__(driver)

    def is_account_heading_displayed(self):
        """Verifies if 'My Account' heading is displayed."""
        return self.is_element_displayed(self.ACCOUNT_HEADING, timeout=10)

    def get_heading_text(self):
        """Returns the heading text of the Account page."""
        return self.get_text(self.ACCOUNT_HEADING)

    def is_edit_account_link_displayed(self):
        """Verifies if the 'Edit your account information' link is visible."""
        return self.is_element_displayed(self.EDIT_ACCOUNT_LINK)

    def logout(self):
        """Clicks logout from the right column navigation."""
        self.logger.info("Logging out from account")
        self.click(self.LOGOUT_LINK)
        return self.is_element_displayed(self.LOGOUT_HEADER)
