import streamlit as st
from app.ui.utils import get_controller

def render(navigate_to):
    st.title("Add New Stock")
    ctrl = get_controller()

    if st.button("← Back to Dashboard"):
        _reset_state()
        navigate_to("dashboard")

    # Initialize state variables for this page
    if "add_stage" not in st.session_state:
        st.session_state.add_stage = "input" # input, confirm_direct, manual_ticker
    if "resolved_data" not in st.session_state:
        st.session_state.resolved_data = {}

    if st.session_state.add_stage == "input":
        st.markdown("Enter a Stock Ticker (e.g., `AAPL`) or ISIN (e.g., `US0378331005`).")
        with st.form("identifier_form"):
            identifier = st.text_input("Identifier")
            submit = st.form_submit_button("Analyze")

        if submit and identifier:
            ticker, isin = ctrl.resolve_identifier(identifier)
            if ticker:
                st.session_state.resolved_data = {"ticker": ticker, "isin": isin}
                st.session_state.add_stage = "confirm_direct"
                st.rerun()
            else:
                st.session_state.resolved_data = {"isin": isin}
                st.session_state.add_stage = "manual_ticker"
                st.rerun()

    elif st.session_state.add_stage == "confirm_direct":
        ticker = st.session_state.resolved_data["ticker"]
        st.info(f"Identified Ticker: **{ticker}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm and Add", type="primary"):
                _add_stock(ctrl, ticker, st.session_state.resolved_data["isin"], navigate_to)
        with col2:
            if st.button("Cancel"):
                _reset_state()
                st.rerun()

    elif st.session_state.add_stage == "manual_ticker":
        isin = st.session_state.resolved_data["isin"]
        st.warning(f"Could not resolve ISIN `{isin}` to a Ticker automatically.")
        st.info("Please enter the Ticker Symbol manually (required for data fetching).")

        with st.form("manual_ticker_form"):
            manual_ticker = st.text_input("Ticker Symbol", placeholder="e.g. AAPL")
            confirm = st.form_submit_button("Add Stock")

        if confirm and manual_ticker:
            _add_stock(ctrl, manual_ticker, isin, navigate_to)

        if st.button("Cancel"):
            _reset_state()
            st.rerun()

def _add_stock(ctrl, ticker, isin, navigate_to):
    with st.spinner(f"Fetching data for {ticker}..."):
        try:
            ctrl.add_stock(ticker, isin)
            st.success(f"Successfully added {ticker}!")
            # Reset state so next time we start fresh
            _reset_state()
            # We can't immediately navigate because we are inside a button callback (mostly)
            # But we can update session state
            st.session_state.view = "dashboard"
            st.rerun()
        except Exception as e:
            st.error(f"Error adding stock: {e}")

def _reset_state():
    if "add_stage" in st.session_state:
        del st.session_state.add_stage
    if "resolved_data" in st.session_state:
        del st.session_state.resolved_data
