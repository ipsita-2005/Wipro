from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.search_page import SearchPage

class HomePage(BasePage):
    """Page Object for the TutorialsNinja Home Page."""

    # Locators
    SEARCH_INPUT = (By.NAME, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    MY_ACCOUNT_DROPDOWN = (By.XPATH, "//span[text()='My Account']")
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    HOME_LOGO = (By.CSS_SELECTOR, "#logo a")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_login_page(self):
        """Clicks on 'My Account' dropdown and selects 'Login'."""
        self.logger.info("Navigating to Login page from Home page")
        self.click(self.MY_ACCOUNT_DROPDOWN)
        self.click(self.LOGIN_LINK)
        return LoginPage(self.driver)

    def navigate_to_register_page(self):
        """Clicks on 'My Account' dropdown and selects 'Register'."""
        self.logger.info("Navigating to Register page from Home page")
        self.click(self.MY_ACCOUNT_DROPDOWN)
        self.click(self.REGISTER_LINK)

    def search_for_product(self, product_name):
        """Enters product name in header search box and clicks search button."""
        self.logger.info(f"Searching for product: '{product_name}'")
        self.send_keys(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)
        return SearchPage(self.driver)

    def is_logo_displayed(self):
        return self.is_element_displayed(self.HOME_LOGO)
