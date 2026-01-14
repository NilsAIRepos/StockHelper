from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import pandas as pd

class StockDataSource(ABC):
    @abstractmethod
    def get_ticker_info(self, ticker: str) -> Dict[str, Any]:
        """Fetch metadata about the stock (name, sector, etc.)"""
        pass

    @abstractmethod
    def get_price_history(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        """Fetch historical price data"""
        pass

    @abstractmethod
    def get_financials(self, ticker: str) -> Dict[str, Any]:
        """Fetch financial statements/info"""
        pass
