import streamlit as st
from app.ui.utils import get_controller
from app.core.api.alpha_vantage import AlphaVantageSource
from app.core.api.polygon import PolygonSource
from app.core.api.finnhub import FinnhubSource
from app.core.api.yfinance_source import YFinanceSource

def render(navigate_to):
    st.title("Settings")

    ctrl = get_controller()
    config = ctrl.config

    # Current values
    current_source = config.get("api_source", "yfinance")
    api_keys = config.get("api_keys", {})

    st.subheader("Data Source Configuration")

    source_options = ["yfinance", "alpha_vantage", "polygon", "finnhub"]
    selected_source = st.selectbox(
        "Select Data Source",
        source_options,
        index=source_options.index(current_source) if current_source in source_options else 0
    )

    st.markdown("---")
    st.subheader("API Keys")
    st.caption("Enter keys for the services you wish to use.")

    av_key = st.text_input("Alpha Vantage Key", value=api_keys.get("alpha_vantage", ""), type="password")
    poly_key = st.text_input("Polygon.io Key", value=api_keys.get("polygon", ""), type="password")
    finn_key = st.text_input("Finnhub Key", value=api_keys.get("finnhub", ""), type="password")

    # Test Connection Section
    st.markdown("---")
    st.subheader("Test Connection")

    test_col1, test_col2 = st.columns([1, 3])
    with test_col1:
        if st.button("Test Configuration"):
            with st.spinner(f"Testing connection to {selected_source}..."):
                try:
                    # Instantiate source based on current inputs (not saved config)
                    source = None
                    if selected_source == "yfinance":
                        source = YFinanceSource()
                    elif selected_source == "alpha_vantage":
                        if not av_key:
                            st.error("Please enter an Alpha Vantage API Key.")
                        else:
                            source = AlphaVantageSource(av_key)
                    elif selected_source == "polygon":
                        if not poly_key:
                            st.error("Please enter a Polygon.io API Key.")
                        else:
                            source = PolygonSource(poly_key)
                    elif selected_source == "finnhub":
                        if not finn_key:
                            st.error("Please enter a Finnhub API Key.")
                        else:
                            source = FinnhubSource(finn_key)

                    if source:
                        # Test with a standard ticker
                        info = source.get_ticker_info("AAPL")
                        st.success(f"Connection Successful! Fetched info for: {info.get('name')}")
                        st.json(info)

                except Exception as e:
                    st.error(f"Connection Failed: {e}")

    # Save Section
    st.markdown("---")
    if st.button("Save Settings", type="primary"):
        new_keys = {
            "alpha_vantage": av_key,
            "polygon": poly_key,
            "finnhub": finn_key
        }

        # Save to config
        config.set("api_source", selected_source)
        config.set("api_keys", new_keys)

        # Reload controller
        ctrl.reload_api_source()

        st.success("Settings saved successfully and API source reloaded.")
