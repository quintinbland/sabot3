# Imports
import streamlit as st
from pathlib import Path
from st_functions import st_button, load_css
from PIL import Image
import pandas as pd

st.set_page_config(layout="wide", page_title="Sabot")

st.title("SaBot Tokenomics")
st.markdown("---")

st.markdown("<h3 style='text-align: left; color: light grey;'>CLOG</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: light grey;'>ERC20 Utility Token.</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: left; color: light grey;'>Purpose</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: light grey;'>Fund the automated trading bot.</p>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: left; color: light grey;'>Initial Exchange Rate</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: light grey;'>1 USDT = 1 CLOG</p>", unsafe_allow_html=True)
st.caption("Subsequent staking will be at prevailing clog price.")
st.markdown("<h3 style='text-align: left; color: light grey;'>CLOG Price</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: light grey;'>As the porfolio value increases, the price of the clog upon staking will adjust to reflect change in portfolio value.</p>", unsafe_allow_html=True)
st.latex(r'''Clog Price = \left(\frac{Portfolio Value}{Total Clog Supply}\right)''')
