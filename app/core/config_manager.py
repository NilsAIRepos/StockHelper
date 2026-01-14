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
                "storage_path": "data/companies",
                "db_path": "data/stocks.db"
            }

    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

    @property
    def storage_path(self) -> str:
        return self.get("storage_path", "data/companies")

    @property
    def db_path(self) -> str:
        return self.get("db_path", "data/stocks.db")
