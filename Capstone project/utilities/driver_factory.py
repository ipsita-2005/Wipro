from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from configurations.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class DriverFactory:
    """Factory to instantiate and configure WebDrivers for various browsers."""

    @staticmethod
    def get_driver(browser_name=None, headless=None):
        if browser_name is None:
            browser_name = ConfigReader.get_browser_name()
        if headless is None:
            headless = ConfigReader.get_headless()

        browser_name = browser_name.lower()
        width, height = ConfigReader.get_window_size()
        implicit_wait = ConfigReader.get_implicit_wait()
        page_load_timeout = ConfigReader.get_page_load_timeout()

        logger.info(f"Initializing WebDriver: Browser={browser_name}, Headless={headless}")

        driver = None
        if browser_name == "chrome":
            options = ChromeOptions()
            options.page_load_strategy = "eager"
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument(f"--window-size={width},{height}")
            options.add_argument("--disable-notifications")
            options.add_argument("--ignore-certificate-errors")
            driver = webdriver.Chrome(options=options)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.page_load_strategy = "eager"
            if headless:
                options.add_argument("-headless")
            options.add_argument(f"--width={width}")
            options.add_argument(f"--height={height}")
            driver = webdriver.Firefox(options=options)

        elif browser_name in ("edge", "msedge"):
            options = EdgeOptions()
            options.page_load_strategy = "eager"
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument(f"--window-size={width},{height}")
            driver = webdriver.Edge(options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser_name}. Supported: chrome, firefox, edge.")

        driver.implicitly_wait(implicit_wait)
        driver.set_page_load_timeout(page_load_timeout)
        if not headless:
            driver.maximize_window()

        logger.info(f"{browser_name.capitalize()} WebDriver initialized successfully.")
        return driver
