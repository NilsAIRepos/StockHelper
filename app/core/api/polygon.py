import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from .base import StockDataSource

class PolygonSource(StockDataSource):
    BASE_URL = "https://api.polygon.io"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get_json(self, endpoint: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        params["apiKey"] = self.api_key
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, params=params)
            # Polygon returns 401/403 for unauthorized/plan limits
            if response.status_code == 403 or response.status_code == 401:
                raise ValueError(f"Polygon API Unauthorized/Forbidden: {response.text}")
            if response.status_code == 429:
                raise ValueError("Polygon API Rate Limit Exceeded")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
             raise ValueError(f"Network error fetching data from Polygon: {e}")

    def get_ticker_info(self, ticker: str) -> Dict[str, Any]:
        endpoint = f"/v3/reference/tickers/{ticker}"
        data = self._get_json(endpoint)

        results = data.get("results", {})
        if not results:
            raise ValueError(f"No info found for ticker {ticker}")

        return {
            "name": results.get("name"),
            "sector": results.get("sic_description"), # rough proxy if sector not explicit
            "industry": results.get("sic_description"),
            "country": results.get("locale", "").upper(),
            "currency": results.get("currency_name"),
            "website": results.get("homepage_url"),
            "summary": results.get("description"),
            "full_info": results
        }

    def get_price_history(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        # Calc dates
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365) # default 1y
        if period == "1y":
            start_date = end_date - timedelta(days=365)
        # Add other period logic if needed

        from_str = start_date.strftime("%Y-%m-%d")
        to_str = end_date.strftime("%Y-%m-%d")

        endpoint = f"/v2/aggs/ticker/{ticker}/range/1/day/{from_str}/{to_str}"
        params = {"sort": "asc", "limit": 50000}

        data = self._get_json(endpoint, params)

        results = data.get("results", [])
        if not results:
             raise ValueError(f"No price data found for {ticker}")

        df = pd.DataFrame(results)
        # Polygon columns: v, vw, o, c, h, l, t, n
        df = df.rename(columns={
            "o": "Open",
            "h": "High",
            "l": "Low",
            "c": "Close",
            "v": "Volume",
            "t": "Date"
        })
        df["Date"] = pd.to_datetime(df["Date"], unit="ms")
        df.set_index("Date", inplace=True)
        return df

    def get_financials(self, ticker: str) -> Dict[str, Any]:
        # /vX/reference/financials
        endpoint = "/vX/reference/financials"
        params = {"ticker": ticker, "limit": 5}

        data = {}
        try:
            res = self._get_json(endpoint, params)
            results = res.get("results", [])
            # Store the raw results list
            data["financials_raw"] = results

            # Attempt to split into standard keys if possible, but structure is different
            # Polygon returns a list of objects, each containing financials for a period.
            data["full_report"] = results

        except Exception as e:
            # Likely plan limitation
            print(f"Error fetching financials for {ticker} from Polygon: {e}")
            data["error"] = str(e)

        return data
