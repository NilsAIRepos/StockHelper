import requests
import pandas as pd
from datetime import datetime
from typing import Dict, Any, Optional
from .base import StockDataSource

class FinnhubSource(StockDataSource):
    BASE_URL = "https://finnhub.io/api/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _get_json(self, endpoint: str, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        params["token"] = self.api_key
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, params=params)
            if response.status_code == 429:
                raise ValueError("Finnhub API Rate Limit Exceeded")
            if response.status_code == 403 or response.status_code == 401:
                 raise ValueError("Finnhub API Unauthorized/Forbidden")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Network error fetching data from Finnhub: {e}")

    def get_ticker_info(self, ticker: str) -> Dict[str, Any]:
        endpoint = "/stock/profile2"
        params = {"symbol": ticker}
        data = self._get_json(endpoint, params)

        if not data:
            raise ValueError(f"No info found for ticker {ticker}")

        return {
            "name": data.get("name"),
            "sector": data.get("finnhubIndustry"),
            "industry": data.get("finnhubIndustry"),
            "country": data.get("country"),
            "currency": data.get("currency"),
            "website": data.get("weburl"),
            "summary": "N/A", # Finnhub profile2 doesn't have summary
            "full_info": data
        }

    def get_price_history(self, ticker: str, period: str = "1y") -> pd.DataFrame:
        # /stock/candle?symbol=...&resolution=D&from=...&to=...
        endpoint = "/stock/candle"

        end_date = datetime.now()

        # Calculate start_date based on period
        if period == "1d":
            start_date = end_date - pd.DateOffset(days=1)
        elif period == "5d":
            start_date = end_date - pd.DateOffset(days=5)
        elif period == "1mo":
            start_date = end_date - pd.DateOffset(months=1)
        elif period == "3mo":
            start_date = end_date - pd.DateOffset(months=3)
        elif period == "6mo":
            start_date = end_date - pd.DateOffset(months=6)
        elif period == "1y":
            start_date = end_date - pd.DateOffset(years=1)
        elif period == "2y":
            start_date = end_date - pd.DateOffset(years=2)
        elif period == "5y":
            start_date = end_date - pd.DateOffset(years=5)
        elif period == "10y":
            start_date = end_date - pd.DateOffset(years=10)
        elif period == "ytd":
            start_date = datetime(end_date.year, 1, 1)
        else:
            # Default to 1y for safety or 'max' (Finnhub 'max' requires knowing IPO date, so just do 20 years)
            start_date = end_date - pd.DateOffset(years=1)

        # timestamps in seconds
        from_ts = int(start_date.timestamp())
        to_ts = int(end_date.timestamp())

        params = {
            "symbol": ticker,
            "resolution": "D",
            "from": from_ts,
            "to": to_ts
        }

        data = self._get_json(endpoint, params)

        if data.get("s") == "no_data":
             raise ValueError(f"No price data found for {ticker}")

        # c: close, h: high, l: low, o: open, t: time, v: volume
        df = pd.DataFrame(data)
        df = df.rename(columns={
            "o": "Open",
            "h": "High",
            "l": "Low",
            "c": "Close",
            "v": "Volume",
            "t": "Date"
        })

        df["Date"] = pd.to_datetime(df["Date"], unit="s")
        df.set_index("Date", inplace=True)
        return df

    def get_financials(self, ticker: str) -> Dict[str, Any]:
        # /stock/financials-reported?symbol=...
        endpoint = "/stock/financials-reported"
        params = {"symbol": ticker}

        data = {}
        try:
            res = self._get_json(endpoint, params)
            data["financials_reported"] = res.get("data", [])

            # Also try "metric" for basic fundamentals if available
            metric_endpoint = "/stock/metric"
            metric_params = {"symbol": ticker, "metric": "all"}
            try:
                metric_res = self._get_json(metric_endpoint, metric_params)
                data["basic_financials"] = metric_res.get("metric", {})
            except:
                pass

        except Exception as e:
            print(f"Error fetching financials for {ticker} from Finnhub: {e}")
            data["error"] = str(e)

        return data
