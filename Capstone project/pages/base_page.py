from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from configurations.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger
from utilities.screenshot_util import ScreenshotUtil

class BasePage:
    """BasePage contains reusable element interactions, synchronization, and logging."""

    def __init__(self, driver):
        self.driver = driver
        self.explicit_wait = ConfigReader.get_explicit_wait()
        self.logger = CustomLogger.get_logger(self.__class__.__name__)

    def open_url(self, url):
        self.logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def get_title(self):
        title = self.driver.title
        self.logger.debug(f"Retrieved page title: '{title}'")
        return title

    def get_current_url(self):
        current_url = self.driver.current_url
        self.logger.debug(f"Retrieved current URL: '{current_url}'")
        return current_url

    def find(self, locator, timeout=None):
        wait_time = timeout if timeout is not None else self.explicit_wait
        try:
            return WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(f"Timed out waiting for element located by: {locator}")
            raise

    def find_elements(self, locator, timeout=None):
        wait_time = timeout if timeout is not None else self.explicit_wait
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            self.logger.warning(f"No elements found for locator: {locator}")
            return []

    def click(self, locator, timeout=None):
        wait_time = timeout if timeout is not None else self.explicit_wait
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(locator)
            )
            self.logger.info(f"Clicking element: {locator}")
            element.click()
        except Exception as e:
            self.logger.error(f"Failed to click element {locator}: {e}")
            raise

    def send_keys(self, locator, text, clear_first=True, timeout=None):
        wait_time = timeout if timeout is not None else self.explicit_wait
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            if clear_first:
                element.clear()
            self.logger.info(f"Entering text '{text}' into element: {locator}")
            element.send_keys(text)
        except Exception as e:
            self.logger.error(f"Failed to send keys to element {locator}: {e}")
            raise

    def get_text(self, locator, timeout=None):
        wait_time = timeout if timeout is not None else self.explicit_wait
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            text = element.text.strip()
            self.logger.debug(f"Read text '{text}' from element: {locator}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get text from element {locator}: {e}")
            raise

    def is_element_displayed(self, locator, timeout=5):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            displayed = element.is_displayed()
            self.logger.debug(f"Element {locator} is displayed: {displayed}")
            return displayed
        except (TimeoutException, NoSuchElementException):
            self.logger.debug(f"Element {locator} is not displayed within {timeout}s.")
            return False

    def scroll_to_element(self, locator):
        try:
            element = self.find(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        except Exception as e:
            self.logger.warning(f"Failed to scroll to element {locator}: {e}")

    def take_screenshot(self, name_prefix="step"):
        return ScreenshotUtil.capture_screenshot(self.driver, name_prefix)
