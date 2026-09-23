import logging
import os
from pathlib import Path
from configurations.config_reader import ConfigReader

class CustomLogger:
    """Configures and provides a singleton logger instance for framework execution."""

    _logger = None

    @classmethod
    def get_logger(cls, name=__name__):
        parent_logger = logging.getLogger("Framework")
        parent_logger.setLevel(logging.DEBUG)

        # Avoid duplicate handlers if already added
        if not parent_logger.handlers:
            log_dir = ConfigReader.get_path("logs_dir")
            log_file = Path(log_dir) / "automation.log"

            # Formatter
            formatter = logging.Formatter(
                fmt="%(asctime)s - [%(levelname)s] - [%(name)s] (%(filename)s:%(lineno)d) : %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # File Handler
            file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            parent_logger.addHandler(file_handler)

            # Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            parent_logger.addHandler(console_handler)

        cls._logger = parent_logger
        clean_name = name if name.startswith("Framework.") else f"Framework.{name}"
        return logging.getLogger(clean_name)
