import os
import sys
sys.path.append(os.getcwd())

from app.core.api.yfinance_source import YFinanceSource

def test_yfinance():
    yf_source = YFinanceSource()
    ticker = "MSFT"

    print(f"Fetching info for {ticker}...")
    info = yf_source.get_ticker_info(ticker)
    print("Name:", info.get("name"))
    assert info.get("name") is not None

    print("Fetching price history...")
    df = yf_source.get_price_history(ticker, period="5d")
    print(df.head())
    assert not df.empty

    print("Fetching financials...")
    fin = yf_source.get_financials(ticker)
    print("Financials keys:", fin.keys())
    assert "income_statement" in fin

if __name__ == "__main__":
    test_yfinance()
