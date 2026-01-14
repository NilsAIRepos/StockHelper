import streamlit as st
from app.ui.utils import get_controller
import pandas as pd

def render(ticker, navigate_to):
    if not ticker:
        st.error("No ticker selected.")
        if st.button("Back"): navigate_to("dashboard")
        return

    ctrl = get_controller()

    if st.button("← Back to Dashboard"):
        navigate_to("dashboard")

    data = ctrl.get_stock_detail(ticker)
    if not data:
        st.error(f"Could not load data for {ticker}.")
        return

    meta = data["meta"]
    company = data["company_data"] or {}
    prices = data["prices"]

    # Header
    st.title(meta.get("name") or ticker)
    st.caption(f"Ticker: {meta.get('ticker')} | Sector: {meta.get('sector')} | ISIN: {meta.get('isin')}")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Price History", "💰 Financials", "🏢 Company Info"])

    with tab1:
        st.subheader("Stock Price (1 Year)")
        if prices is not None and not prices.empty:
            # Streamlit line chart expects index to be x-axis
            st.line_chart(prices["Close"])
        else:
            st.warning("No price data available.")

        if st.button("Refresh Data"):
             with st.spinner("Fetching latest data..."):
                 ctrl.update_stock_data(ticker)
                 st.rerun()

    with tab2:
        st.subheader("Financial Statements")

        ftype = st.selectbox("Statement Type", ["Income Statement", "Balance Sheet", "Cash Flow"])

        key_map = {
            "Income Statement": "income_statement",
            "Balance Sheet": "balance_sheet",
            "Cash Flow": "cashflow"
        }

        f_data = company.get(key_map[ftype], {})
        if f_data:
            # Convert dict to DF
            df_fin = pd.DataFrame(f_data)
            st.dataframe(df_fin, width="stretch")
        else:
            st.info("No data available for this statement.")

    with tab3:
        st.subheader("Company Profile")
        info = company.get("info", {})
        if info:
            st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
            st.markdown(f"**Website:** {info.get('website', 'N/A')}")

            st.markdown("### Business Summary")
            st.write(info.get("summary", "No summary available."))

            with st.expander("Full Raw Info"):
                st.json(info)
        else:
            st.info("No detailed info available.")
