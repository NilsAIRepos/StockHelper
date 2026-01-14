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
- [ ] **Multi-API Support**: Integrate AlphaVantage or IEX Cloud as alternative data sources.
- [ ] **Enhanced ISIN Resolution**: Implement a more robust lookup service to convert ISIN to Ticker symbols (currently relies on basic resolution or user input).

### Data Management
- [ ] **Manual Editing**: Interface to manually correct or input financial data points.
- [ ] **Historical Data**: Deep history storage and incremental updates.

### Visualization & UI
- [ ] **Advanced Charting**: Interactive candle-stick charts and performance comparison graphs.
- [ ] **Portfolio Tracking**: Calculate total portfolio value and gains/losses.
