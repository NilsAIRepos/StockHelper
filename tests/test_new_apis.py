import unittest
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.append(os.getcwd())

from app.core.api.alpha_vantage import AlphaVantageSource
from app.core.api.polygon import PolygonSource
from app.core.api.finnhub import FinnhubSource
from app.core.api.factory import get_stock_data_source
from app.core.config_manager import ConfigManager
from app.core.api.yfinance_source import YFinanceSource

class TestNewAPIs(unittest.TestCase):
    def test_instantiation(self):
        av = AlphaVantageSource("dummy_key")
        self.assertEqual(av.api_key, "dummy_key")

        poly = PolygonSource("dummy_key")
        self.assertEqual(poly.api_key, "dummy_key")

        finn = FinnhubSource("dummy_key")
        self.assertEqual(finn.api_key, "dummy_key")

    def test_factory_defaults(self):
        # Mock ConfigManager to return default (yfinance)
        mock_config = MagicMock()
        mock_config.get.side_effect = lambda key, default=None: "yfinance" if key == "api_source" else default

        source = get_stock_data_source(mock_config)
        self.assertIsInstance(source, YFinanceSource)

    def test_factory_alpha_vantage(self):
        mock_config = MagicMock()
        def get_side_effect(key, default=None):
            if key == "api_source": return "alpha_vantage"
            if key == "api_keys": return {"alpha_vantage": "key123"}
            return default
        mock_config.get.side_effect = get_side_effect

        source = get_stock_data_source(mock_config)
        self.assertIsInstance(source, AlphaVantageSource)
        self.assertEqual(source.api_key, "key123")

    def test_factory_fallback(self):
        # Test fallback if key is missing
        mock_config = MagicMock()
        def get_side_effect(key, default=None):
            if key == "api_source": return "alpha_vantage"
            if key == "api_keys": return {} # Missing key
            return default
        mock_config.get.side_effect = get_side_effect

        source = get_stock_data_source(mock_config)
        self.assertIsInstance(source, YFinanceSource)

if __name__ == "__main__":
    unittest.main()
