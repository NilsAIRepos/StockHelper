import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from app.core.config_manager import ConfigManager
import pandas as pd

class StorageManager:
    def __init__(self):
        self.config = ConfigManager()
        self.db_path = self.config.db_path
        self.storage_path = self.config.storage_path
        self._initialize_db()
        self._initialize_storage()

    def _initialize_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT UNIQUE NOT NULL,
                isin TEXT,
                name TEXT,
                sector TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def _initialize_storage(self):
        os.makedirs(self.storage_path, exist_ok=True)

    def add_stock(self, ticker: str, isin: Optional[str] = None, name: Optional[str] = None, sector: Optional[str] = None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO stocks (ticker, isin, name, sector)
                VALUES (?, ?, ?, ?)
            ''', (ticker, isin, name, sector))
            conn.commit()
        except sqlite3.IntegrityError:
            # Update existing if needed, or just ignore
            print(f"Stock {ticker} already exists. Updating details.")
            cursor.execute('''
                UPDATE stocks SET isin = COALESCE(?, isin), name = COALESCE(?, name), sector = COALESCE(?, sector)
                WHERE ticker = ?
            ''', (isin, name, sector, ticker))
            conn.commit()
        finally:
            conn.close()

    def get_stocks(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM stocks')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_stock(self, ticker: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM stocks WHERE ticker = ?', (ticker,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def save_company_data(self, ticker: str, data: Dict[str, Any]):
        """Saves fundamental company data to a JSON file."""
        filepath = os.path.join(self.storage_path, f"{ticker}_data.json")
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def load_company_data(self, ticker: str) -> Optional[Dict[str, Any]]:
        filepath = os.path.join(self.storage_path, f"{ticker}_data.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
        return None

    def save_price_data(self, ticker: str, df: pd.DataFrame):
        """Saves price history to a CSV or JSON file."""
        # Using CSV for time series might be cleaner for viewing, but user asked for 'company data in one file... prices locally'.
        # Let's separate prices to a different file to avoid massive JSONs.
        # But 'fetching company performance data and save it locally... Fetching stock price data and save it locally'
        # I'll stick to a separate file for prices: {ticker}_prices.csv
        filepath = os.path.join(self.storage_path, f"{ticker}_prices.csv")
        df.to_csv(filepath)

    def load_price_data(self, ticker: str) -> Optional[pd.DataFrame]:
        filepath = os.path.join(self.storage_path, f"{ticker}_prices.csv")
        if os.path.exists(filepath):
            return pd.read_csv(filepath, index_col=0, parse_dates=True)
        return None
