import pytest
from pathlib import Path
from pages.home_page import HomePage
from utilities.csv_reader import CSVReader
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("TestSearchPytest")

# Path to search test data
SEARCH_CSV_PATH = Path(__file__).resolve().parent.parent / "test_data" / "search_data.csv"
SEARCH_TEST_DATA = CSVReader.get_csv_rows_as_tuples(str(SEARCH_CSV_PATH))

class TestSearchPytest:
    """Test suite for Product Search functionality using PyTest and POM."""

    @pytest.mark.smoke
    @pytest.mark.search
    def test_search_existing_product(self, driver):
        """TC_SEARCH_01: Verify searching for an existing product displays matching results."""
        logger.info("Executing test_search_existing_product")
        home_page = HomePage(driver)
        search_page = home_page.search_for_product("MacBook")

        assert search_page.is_search_page_displayed(), "Search results page was not displayed."
        products = search_page.get_product_names()
        assert len(products) > 0, "Expected at least 1 product in search results, but found none."
        assert search_page.is_product_displayed("MacBook"), "Expected 'MacBook' in product search results."

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_non_existing_product(self, driver):
        """TC_SEARCH_02: Verify searching for a non-existing product displays appropriate no-match message."""
        logger.info("Executing test_search_non_existing_product")
        home_page = HomePage(driver)
        search_page = home_page.search_for_product("NonExistingLaptop999XYZ")

        assert search_page.is_no_product_message_displayed(), "No-product message was not displayed."
        no_match_msg = search_page.get_no_product_message_text()
        assert "There is no product that matches the search criteria." in no_match_msg, (
            f"Unexpected message received: '{no_match_msg}'"
        )
        assert search_page.get_products_count() == 0, "Expected 0 product cards for non-existing search query."

    @pytest.mark.regression
    @pytest.mark.search
    def test_search_empty_query(self, driver):
        """TC_SEARCH_03: Verify searching without entering any query displays criteria message."""
        logger.info("Executing test_search_empty_query")
        home_page = HomePage(driver)
        search_page = home_page.search_for_product("")

        assert search_page.is_no_product_message_displayed(), "No-product message was not displayed on empty search."
        assert "There is no product that matches the search criteria." in search_page.get_no_product_message_text()

    @pytest.mark.datadriven
    @pytest.mark.search
    @pytest.mark.parametrize("tc_id, search_term, expected_status, expected_result", SEARCH_TEST_DATA)
    def test_data_driven_search(self, driver, tc_id, search_term, expected_status, expected_result):
        """TC_SEARCH_DDT: Data-driven product search executing across all records in CSV."""
        logger.info(f"Executing {tc_id} with search_term: '{search_term}', status: '{expected_status}'")
        home_page = HomePage(driver)
        search_page = home_page.search_for_product(search_term)

        if expected_status == "found":
            assert search_page.is_product_displayed(expected_result), (
                f"Product '{expected_result}' was not found in results for {tc_id}."
            )
        elif expected_status == "not_found":
            assert search_page.is_no_product_message_displayed(), (
                f"No-product message was missing for {tc_id}."
            )
            assert expected_result in search_page.get_no_product_message_text()
