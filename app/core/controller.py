from typing import Optional, Tuple, Dict, Any
from app.core.storage_manager import StorageManager
from app.core.api.yfinance_source import YFinanceSource
from app.core.api.resolver import DataResolver
from app.core.config_manager import ConfigManager

class StockAppController:
    def __init__(self):
        self.config = ConfigManager()
        self.storage = StorageManager()
        self.resolver = DataResolver()
        # In a real app, we might support multiple sources based on config
        self.api = YFinanceSource()

    def get_all_stocks(self):
        return self.storage.get_stocks()

    def get_stock_detail(self, ticker: str):
        stock_meta = self.storage.get_stock(ticker)
        if not stock_meta:
            return None

        company_data = self.storage.load_company_data(ticker)
        prices = self.storage.load_price_data(ticker)
        return {
            "meta": stock_meta,
            "company_data": company_data,
            "prices": prices
        }

    def resolve_identifier(self, identifier: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Returns (ticker, isin).
        """
        return self.resolver.resolve(identifier)

    def add_stock(self, ticker: str, isin: Optional[str] = None) -> bool:
        """
        Adds a stock to the inventory and performs an initial data fetch.
        Raises ValueError if ticker is invalid.
        """
        # 1. Fetch info to validate and get name/sector
        try:
            info = self.api.get_ticker_info(ticker)
        except Exception as e:
            raise ValueError(f"Could not validate ticker '{ticker}': {e}")

        name = info.get("name")
        sector = info.get("sector")

        # 2. Add to DB
        self.storage.add_stock(ticker, isin, name, sector)

        # 3. Initial Data Fetch (Fail-safe, don't crash if fetch fails, just warn)
        try:
            self.update_stock_data(ticker)
        except Exception as e:
            print(f"Warning: Initial data fetch failed for {ticker}: {e}")

        return True

    def update_stock_data(self, ticker: str):
        """Fetches fresh data from API and saves to local storage."""
        # Fetch financials
        fin_data = self.api.get_financials(ticker)
        # Fetch generic info to merge
        info = self.api.get_ticker_info(ticker)
        fin_data["info"] = info # Store all info in the json

        self.storage.save_company_data(ticker, fin_data)

        # Fetch Prices
        prices = self.api.get_price_history(ticker, period="1y")
        self.storage.save_price_data(ticker, prices)
