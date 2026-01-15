import json
import os
from typing import Any, Dict

class ConfigManager:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = os.path.join("config", "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                self._config = json.load(f)
        else:
            # Defaults
            self._config = {
                "api_source": "yfinance",
                "api_keys": {},
                "storage_path": "data/companies",
                "db_path": "data/stocks.db"
            }

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        self._config[key] = value
        self.save_config()

    def save_config(self):
        config_dir = "config"
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        config_path = os.path.join(config_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(self._config, f, indent=4)

    @property
    def storage_path(self) -> str:
        return self.get("storage_path", "data/companies")

    @property
    def db_path(self) -> str:
        return self.get("db_path", "data/stocks.db")
