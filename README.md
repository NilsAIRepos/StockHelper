# StockHelper

A modern Python web application to track stock performance and prices.

## Features (Skeleton Implemented)
- **Stock Inventory**: Add and manage stocks using Ticker or ISIN.
- **Data Fetching**: automated data retrieval using `yfinance`.
- **Local Storage**: Data persistence using JSON files for individual company data and SQLite for the inventory.
- **Visualization**: Basic dashboard to view tracked stocks.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   streamlit run app/main.py
   ```

## Roadmap

### Data Acquisition
- [x] **Multi-API Support**: Integrated Alpha Vantage, Polygon.io, and Finnhub as alternative data sources.
- [ ] **Enhanced ISIN Resolution**: Implement a more robust lookup service to convert ISIN to Ticker symbols (currently relies on basic resolution or user input).

#### Alternative Data Sources (Reputable Free APIs)

Here is a list of APIs researched for potential integration:

1.  **Alpha Vantage**
    *   **Limits**: Free tier has 25 requests/day.
    *   **Data Types**: Stocks, Forex, Crypto, Technical Indicators, Fundamentals.
    *   **Documentation**: [Alpha Vantage Docs](https://www.alphavantage.co/documentation/)
2.  **Polygon.io**
    *   **Limits**: 5 API calls/minute, End-of-Day data only (delayed), 2 years history.
    *   **Data Types**: Stocks, Options, Forex, Crypto.
    *   **Documentation**: [Polygon.io Docs](https://polygon.io/docs/stocks/getting-started)
3.  **Finnhub**
    *   **Limits**: 60 API calls/minute.
    *   **Data Types**: Global stocks, ETFs, financials, sentiment.
    *   **Documentation**: [Finnhub Docs](https://finnhub.io/docs/api)
4.  **Twelve Data**
    *   **Limits**: 800 API calls/day, 8/minute.
    *   **Data Types**: Real-time & historical, stocks, forex, crypto.
    *   **Documentation**: [Twelve Data Docs](https://twelvedata.com/docs)
5.  **MarketStack**
    *   **Limits**: 100 requests/month.
    *   **Data Types**: Real-time, intraday, historical data.
    *   **Documentation**: [MarketStack Docs](https://marketstack.com/documentation)
6.  **Tiingo**
    *   **Limits**: 50 requests/hour, 1000/day.
    *   **Data Types**: End-of-Day prices, News, Crypto.
    *   **Documentation**: [Tiingo Docs](https://api.tiingo.com/docs)
7.  **EOD Historical Data**
    *   **Limits**: 20 requests/day.
    *   **Data Types**: Historical prices, fundamentals.
    *   **Documentation**: [EOD Historical Data Docs](https://eodhistoricaldata.com/cp/settings)

### Data Management
- [ ] **Manual Editing**: Interface to manually correct or input financial data points.
- [ ] **Historical Data**: Deep history storage and incremental updates.

### Visualization & UI
- [ ] **Advanced Charting**: Interactive candle-stick charts and performance comparison graphs.
- [ ] **Portfolio Tracking**: Calculate total portfolio value and gains/losses.
