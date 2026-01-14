import streamlit as st
import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from app.ui import dashboard, add_stock, details

st.set_page_config(page_title="StockHelper", layout="wide", page_icon="📈")

# Simple routing using session state
if "view" not in st.session_state:
    st.session_state.view = "dashboard"
if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = None

def navigate_to(view, ticker=None):
    st.session_state.view = view
    st.session_state.selected_ticker = ticker
    st.rerun()

# Sidebar
st.sidebar.title("📈 StockHelper")

if st.sidebar.button("📊 Dashboard", use_container_width=True):
    navigate_to("dashboard")

if st.sidebar.button("➕ Add Stock", use_container_width=True):
    navigate_to("add_stock")

st.sidebar.markdown("---")
st.sidebar.caption("Data Source: Yahoo Finance")

# Main Content
if st.session_state.view == "dashboard":
    dashboard.render(navigate_to)
elif st.session_state.view == "add_stock":
    add_stock.render(navigate_to)
elif st.session_state.view == "details":
    details.render(st.session_state.selected_ticker, navigate_to)
