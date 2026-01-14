import yfinance as yf
import pandas as pd
from typing import Dict, Any
from .base import StockDataSource

class YFinanceSource(StockDataSource):
    def get_ticker_info(self, ticker: str) -> Dict[str, Any]:
        t = yf.Ticker(ticker)
        # yfinance info can be slow or flaky, but it's what we have.
        info = t.info
        if not info:
             raise ValueError(f"Could not fetch info for ticker {ticker}")

        # Extract relevant fields to keep it clean, or return all
        return {
            "name": info.get("longName") or info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "currency": info.get("currency"),
            "website": info.get("website"),
            "summary": info.get("longBusinessSummary"),
            # Add more as needed
            "full_info": info
        }

    def get_price_history(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        t = yf.Ticker(ticker)
        df = t.history(period=period)
        if df.empty:
            raise ValueError(f"No price data found for {ticker}")
        return df

    def get_financials(self, ticker: str) -> Dict[str, Any]:
        t = yf.Ticker(ticker)
        # financials, balance_sheet, cashflow are dataframes
        # convert to dict for storage
        data = {}

        def safe_to_dict(df):
            if df.empty: return {}
            # Convert column names (Timestamps) to strings
            # We use a copy to avoid modifying the original dataframe which might be cached/used elsewhere
            df = df.copy()
            df.columns = df.columns.astype(str)
            return df.to_dict()

        try:
            data["income_statement"] = safe_to_dict(t.financials)
            data["balance_sheet"] = safe_to_dict(t.balance_sheet)
            data["cashflow"] = safe_to_dict(t.cashflow)
        except Exception as e:
            print(f"Error fetching financials for {ticker}: {e}")

        return data
