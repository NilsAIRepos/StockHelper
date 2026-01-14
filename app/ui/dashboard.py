import streamlit as st
from app.ui.utils import get_controller
import pandas as pd

def render(navigate_to):
    st.title("Your Watchlist")

    ctrl = get_controller()
    stocks = ctrl.get_all_stocks()

    if not stocks:
        st.info("No stocks in watchlist. Add one to get started!")
        if st.button("Add your first stock"):
            navigate_to("add_stock")
        return

    # Prepare data for display
    data = []
    for s in stocks:
        data.append({
            "Ticker": s["ticker"],
            "Name": s["name"],
            "Sector": s["sector"],
            "ISIN": s["isin"]
        })

    df = pd.DataFrame(data)

    st.markdown("Select a stock to view details.")

    event = st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )

    # Handle selection
    if event and len(event.selection.rows) > 0:
        selected_index = event.selection.rows[0]
        selected_ticker = df.iloc[selected_index]["Ticker"]
        navigate_to("details", selected_ticker)
