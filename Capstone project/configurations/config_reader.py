import os
import configparser
from pathlib import Path

class ConfigReader:
    """Utility class to read configuration properties from config.ini."""
    
    _config = None
    _ini_path = Path(__file__).resolve().parent / "config.ini"

    @classmethod
    def _load_config(cls):
        if cls._config is None:
            cls._config = configparser.ConfigParser()
            if not cls._ini_path.exists():
                raise FileNotFoundError(f"Configuration file not found at: {cls._ini_path}")
            cls._config.read(cls._ini_path, encoding="utf-8")
        return cls._config

    @classmethod
    def get(cls, section, key, fallback=None):
        config = cls._load_config()
        return config.get(section, key, fallback=fallback)

    @classmethod
    def get_boolean(cls, section, key, fallback=False):
        config = cls._load_config()
        return config.getboolean(section, key, fallback=fallback)

    @classmethod
    def get_int(cls, section, key, fallback=0):
        config = cls._load_config()
        return config.getint(section, key, fallback=fallback)

    # Specific property getters
    @classmethod
    def get_base_url(cls):
        return cls.get("common", "base_url", "https://tutorialsninja.com/demo/")

    @classmethod
    def get_browser_name(cls):
        return cls.get("browser", "browser_name", "chrome")

    @classmethod
    def get_headless(cls):
        return cls.get_boolean("browser", "headless", False)

    @classmethod
    def get_window_size(cls):
        width = cls.get_int("browser", "window_width", 1920)
        height = cls.get_int("browser", "window_height", 1080)
        return width, height

    @classmethod
    def get_implicit_wait(cls):
        return cls.get_int("timeouts", "implicit_wait", 10)

    @classmethod
    def get_explicit_wait(cls):
        return cls.get_int("timeouts", "explicit_wait", 15)

    @classmethod
    def get_page_load_timeout(cls):
        return cls.get_int("timeouts", "page_load_timeout", 30)

    @classmethod
    def get_valid_credentials(cls):
        email = cls.get("credentials", "valid_email", "")
        password = cls.get("credentials", "valid_password", "")
        return email, password

    @classmethod
    def get_path(cls, path_key):
        project_root = Path(__file__).resolve().parent.parent
        rel_path = cls.get("paths", path_key, "")
        full_path = project_root / rel_path
        full_path.mkdir(parents=True, exist_ok=True)
        return str(full_path)
