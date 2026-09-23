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

logger = CustomLogger.get_logger("TestSearchUnittest")

SEARCH_CSV_PATH = Path(__file__).resolve().parent.parent / "test_data" / "search_data.csv"

class TestSearchUnittest(unittest.TestCase):
    """Unittest TestCase implementation for Product Search scenarios."""

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

    def test_search_existing_product(self):
        """TC_UNITTEST_SEARCH_01: Verify existing product search returns results."""
        home_page = HomePage(self.driver)
        search_page = home_page.search_for_product("MacBook")

        self.assertTrue(search_page.is_search_page_displayed(), "Search page was not displayed.")
        self.assertTrue(search_page.is_product_displayed("MacBook"), "Product 'MacBook' not found in results.")
        self.assertGreater(search_page.get_products_count(), 0, "Product count should be greater than 0.")

    def test_search_non_existing_product(self):
        """TC_UNITTEST_SEARCH_02: Verify no-match message for non-existing product query."""
        home_page = HomePage(self.driver)
        search_page = home_page.search_for_product("NonExistingLaptop999XYZ")

        self.assertTrue(search_page.is_no_product_message_displayed(), "No-product message was not shown.")
        self.assertIn("There is no product that matches the search criteria.", search_page.get_no_product_message_text())
        self.assertEqual(search_page.get_products_count(), 0, "Product count should be 0.")

    def test_search_empty_query(self):
        """TC_UNITTEST_SEARCH_03: Verify message when search submitted with empty query."""
        home_page = HomePage(self.driver)
        search_page = home_page.search_for_product("")

        self.assertTrue(search_page.is_no_product_message_displayed(), "No-product message was not shown on empty search.")
        self.assertIn("There is no product that matches the search criteria.", search_page.get_no_product_message_text())

    def test_data_driven_search_from_csv(self):
        """TC_UNITTEST_SEARCH_DDT: Executes search across all records in search_data.csv."""
        records = CSVReader.get_csv_rows_as_tuples(str(SEARCH_CSV_PATH))
        for tc_id, search_term, expected_status, expected_result in records:
            with self.subTest(test_case_id=tc_id, search_term=search_term):
                logger.info(f"Running search subtest {tc_id} for term: '{search_term}'")
                self.driver.get(self.base_url)
                home_page = HomePage(self.driver)
                search_page = home_page.search_for_product(search_term)

                if expected_status == "found":
                    self.assertTrue(search_page.is_product_displayed(expected_result), f"Product '{expected_result}' not found in {tc_id}")
                elif expected_status == "not_found":
                    self.assertTrue(search_page.is_no_product_message_displayed(), f"No-product message missing in {tc_id}")
                    self.assertIn(expected_result, search_page.get_no_product_message_text())

if __name__ == "__main__":
    unittest.main()
