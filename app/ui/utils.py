import streamlit as st
from app.core.controller import StockAppController

@st.cache_resource
def get_controller():
    return StockAppController()
