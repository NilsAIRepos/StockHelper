from typing import Dict, Any
from app.core.config_manager import ConfigManager
from .base import StockDataSource
from .yfinance_source import YFinanceSource
from .alpha_vantage import AlphaVantageSource
from .polygon import PolygonSource
from .finnhub import FinnhubSource

def get_stock_data_source(config_manager: ConfigManager) -> StockDataSource:
    source_name = config_manager.get("api_source", "yfinance")
    api_keys = config_manager.get("api_keys", {})

    if source_name == "alpha_vantage":
        key = api_keys.get("alpha_vantage")
        if key:
            return AlphaVantageSource(key)
        else:
            print("Warning: Alpha Vantage selected but no key found. Falling back to YFinance.")

    elif source_name == "polygon":
        key = api_keys.get("polygon")
        if key:
            return PolygonSource(key)
        else:
            print("Warning: Polygon selected but no key found. Falling back to YFinance.")

    elif source_name == "finnhub":
        key = api_keys.get("finnhub")
        if key:
            return FinnhubSource(key)
        else:
            print("Warning: Finnhub selected but no key found. Falling back to YFinance.")

    return YFinanceSource()
