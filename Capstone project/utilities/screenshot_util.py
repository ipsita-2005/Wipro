import os
from datetime import datetime
from pathlib import Path
from configurations.config_reader import ConfigReader
from utilities.custom_logger import CustomLogger

logger = CustomLogger.get_logger(__name__)

class ScreenshotUtil:
    """Helper class to capture and save screenshots with timestamps."""

    @staticmethod
    def capture_screenshot(driver, test_name="screenshot"):
        """Captures a screenshot of the current browser state and returns its absolute path."""
        try:
            screenshots_dir = ConfigReader.get_path("screenshots_dir")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            sanitized_name = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in test_name)
            file_name = f"{sanitized_name}_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)

            driver.save_screenshot(file_path)
            logger.info(f"Screenshot captured successfully: {file_path}")
            return os.path.abspath(file_path)
        except Exception as e:
            logger.error(f"Failed to capture screenshot for '{test_name}': {e}")
            return None
