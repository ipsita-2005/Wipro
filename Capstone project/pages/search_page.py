from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SearchPage(BasePage):
    """Page Object for Product Search results page."""

    # Locators
    SEARCH_INPUT = (By.ID, "input-search")
    SEARCH_BUTTON = (By.ID, "button-search")
    SEARCH_HEADER = (By.XPATH, "//div[@id='content']/h1[contains(text(),'Search')]")
    PRODUCT_TITLES = (By.CSS_SELECTOR, ".product-thumb h4 a")
    PRODUCT_THUMBS = (By.CSS_SELECTOR, ".product-thumb")
    NO_PRODUCT_MESSAGE = (By.XPATH, "//p[contains(text(),'There is no product that matches')]")

    def __init__(self, driver):
        super().__init__(driver)

    def is_search_page_displayed(self):
        """Verifies if the search results page header or search input is displayed."""
        return self.is_element_displayed(self.SEARCH_INPUT)

    def get_product_names(self):
        """Returns a list of all product name strings displayed in the search results."""
        elements = self.find_elements(self.PRODUCT_TITLES)
        product_names = [el.text.strip() for el in elements if el.text.strip()]
        self.logger.info(f"Retrieved {len(product_names)} product(s): {product_names}")
        return product_names

    def is_product_displayed(self, product_name):
        """Checks if a given product name matches any displayed product title (case-insensitive)."""
        products = self.get_product_names()
        is_present = any(product_name.lower() in p.lower() for p in products)
        self.logger.info(f"Product '{product_name}' presence check: {is_present}")
        return is_present

    def get_products_count(self):
        """Returns total count of product cards displayed on the page."""
        count = len(self.find_elements(self.PRODUCT_THUMBS))
        self.logger.info(f"Total product cards count: {count}")
        return count

    def is_no_product_message_displayed(self):
        """Checks if 'There is no product that matches the search criteria.' message is shown."""
        return self.is_element_displayed(self.NO_PRODUCT_MESSAGE, timeout=6)

    def get_no_product_message_text(self):
        """Retrieves text of the 'no products found' message."""
        return self.get_text(self.NO_PRODUCT_MESSAGE)

    def search_again(self, new_keyword):
        """Searches using the inline search box on the search results page."""
        self.logger.info(f"Re-searching with keyword: '{new_keyword}'")
        self.send_keys(self.SEARCH_INPUT, new_keyword)
        self.click(self.SEARCH_BUTTON)
