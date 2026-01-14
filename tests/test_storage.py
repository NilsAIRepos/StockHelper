import os
import sys
# Add project root to path
sys.path.append(os.getcwd())

from app.core.storage_manager import StorageManager
import pandas as pd

def test_storage():
    sm = StorageManager()

    # Test DB
    sm.add_stock("AAPL", "US0378331005", "Apple Inc.")
    stocks = sm.get_stocks()
    print("Stocks in DB:", stocks)
    assert len(stocks) >= 1
    assert stocks[0]['ticker'] == "AAPL"

    # Test File Storage
    data = {"sector": "Technology", "pe_ratio": 30}
    sm.save_company_data("AAPL", data)
    loaded_data = sm.load_company_data("AAPL")
    print("Loaded Data:", loaded_data)
    assert loaded_data['sector'] == "Technology"

    # Test Price Storage
    df = pd.DataFrame({"Close": [150, 155]}, index=pd.to_datetime(["2023-01-01", "2023-01-02"]))
    sm.save_price_data("AAPL", df)
    loaded_df = sm.load_price_data("AAPL")
    print("Loaded Prices:\n", loaded_df)
    assert not loaded_df.empty

if __name__ == "__main__":
    test_storage()
