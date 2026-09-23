import unittest
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_login_unittest import TestLoginUnittest
from tests.test_search_unittest import TestSearchUnittest
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger("UnittestSuiteRunner")

def build_suite():
    """Assembles all Unittest test cases into a TestSuite."""
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    suite.addTests(loader.loadTestsFromTestCase(TestLoginUnittest))
    suite.addTests(loader.loadTestsFromTestCase(TestSearchUnittest))
    return suite

def main():
    print("=" * 70)
    print("  CAPSTONE AUTOMATION: RUNNING UNITTEST SUITE")
    print("=" * 70)

    suite = build_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print("  UNITTEST EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Total Tests Run   : {result.testsRun}")
    print(f"Passed Tests      : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed Tests      : {len(result.failures)}")
    print(f"Errors Encountered: {len(result.errors)}")
    print(f"Success           : {result.wasSuccessful()}")
    print("=" * 70)

    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    main()
