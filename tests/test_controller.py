import os
import sys
sys.path.append(os.getcwd())

from app.core.controller import StockAppController

def test_controller():
    ctrl = StockAppController()

    # Test Resolve
    print("Testing Resolver...")
    ticker, isin = ctrl.resolve_identifier("US0378331005")
    assert ticker is None # Expecting None because we don't have real lookup
    assert isin == "US0378331005"

    ticker, isin = ctrl.resolve_identifier("AAPL")
    assert ticker == "AAPL"
    assert isin is None

    # Test Add Stock
    print("Testing Add Stock (NVDA)...")
    try:
        ctrl.add_stock("NVDA", isin="US67066G1040")
        print("NVDA added successfully.")
    except Exception as e:
        print(f"Failed to add NVDA: {e}")
        raise

    # Verify Data
    details = ctrl.get_stock_detail("NVDA")
    assert details["meta"]["ticker"] == "NVDA"
    assert details["company_data"] is not None
    assert details["prices"] is not None
    print("NVDA details verification passed.")

if __name__ == "__main__":
    test_controller()
