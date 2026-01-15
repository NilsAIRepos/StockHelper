import requests
import pandas as pd
from typing import Dict, Any, Optional
from .base import StockDataSource

class AlphaVantageSource(StockDataSource):
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get_json(self, function: str, symbol: str) -> Dict[str, Any]:
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key
        }
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            # Alpha Vantage returns "Note" or "Information" keys if limit reached or error
            if "Note" in data:
                raise ValueError(f"Alpha Vantage API limit reached: {data['Note']}")
            if "Information" in data:
                raise ValueError(f"Alpha Vantage API Info: {data['Information']}")
            if "Error Message" in data:
                raise ValueError(f"Alpha Vantage API Error: {data['Error Message']}")
            return data
        except requests.RequestException as e:
            raise ValueError(f"Network error fetching data from Alpha Vantage: {e}")

    def get_ticker_info(self, ticker: str) -> Dict[str, Any]:
        data = self._get_json("OVERVIEW", ticker)

        # Check if empty (invalid ticker often returns {})
        if not data:
             raise ValueError(f"No info found for ticker {ticker}")

        return {
            "name": data.get("Name"),
            "sector": data.get("Sector"),
            "industry": data.get("Industry"),
            "country": data.get("Country"),
            "currency": data.get("Currency"),
            "website": "N/A", # AV doesn't return website in Overview
            "summary": data.get("Description"),
            "full_info": data
        }

    def get_price_history(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        # Alpha Vantage TIME_SERIES_DAILY returns default compact (100 days) or full (20+ years)
        # We will use outputsize=full if we want more than 100 days, but 'period' arg is tricky here.
        # For simplicity, we'll request full and filter, or just take what we get.
        # Since the interface asks for 'period', we'll try to support it vaguely,
        # but AV 'compact' is ~5 months.

        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.api_key,
            "outputsize": "full" # Get all data to be safe, filter later
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "Time Series (Daily)" not in data:
                 if "Note" in data: raise ValueError(f"Limit reached: {data['Note']}")
                 raise ValueError(f"No price data found for {ticker}")

            ts_data = data["Time Series (Daily)"]
            df = pd.DataFrame.from_dict(ts_data, orient='index')
            df.index = pd.to_datetime(df.index)
            df = df.rename(columns={
                "1. open": "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "5. volume": "Volume"
            })
            df = df.astype(float)
            df.sort_index(inplace=True)

            # Simple period filtering (very rough approximation)
            if period == "1y":
                start_date = pd.Timestamp.now() - pd.DateOffset(years=1)
                df = df[df.index >= start_date]
            # Add more period logic if needed

            return df

        except requests.RequestException as e:
            raise ValueError(f"Network error: {e}")

    def get_financials(self, ticker: str) -> Dict[str, Any]:
        data = {}

        endpoints = {
            "income_statement": "INCOME_STATEMENT",
            "balance_sheet": "BALANCE_SHEET",
            "cashflow": "CASH_FLOW"
        }

        for key, func in endpoints.items():
            try:
                res = self._get_json(func, ticker)
                # AV returns { "symbol": "...", "annualReports": [...], "quarterlyReports": [...] }
                # We will store the raw list of reports
                if "annualReports" in res:
                    # Convert list of dicts to dict of dicts (keyed by date) or just keep as is?
                    # The interface expects something that can be stored.
                    # yfinance implementation returned a dict (likely from dataframe).
                    # Let's just store the raw list structure for now,
                    # as our app doesn't seem to process it deeply yet.
                    data[key] = res
            except Exception as e:
                print(f"Error fetching {key} for {ticker} from Alpha Vantage: {e}")

        return data
