# Imports
import streamlit as st
from pathlib import Path
from st_functions import st_button, load_css
from PIL import Image
import pandas as pd

st.set_page_config(layout="wide", page_title="Sabot")


st.markdown("---")

col_sol1, col_sol2 = st.columns(2)

with col_sol1:
    st.header("Architecture")
    st.image("./images/sabot_solution_02.png")

with col_sol2:
    st.header("Class Diagram")
    st.image("images/sabot_class_diagram.png")

st.markdown("---")

st.markdown("<h2 style='text-align: left; color: light grey;'>Cost Analysis</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: light grey;'>Exploration of Costs Conducted at the Time of the Analysis.</p>", unsafe_allow_html=True)

GasFee01, GasFee02 = st.columns(2)

GasFee01.metric("GAS FEE", "10 gwei")
GasFee02.metric("","")

GasFee03, GasFee04 = st.columns(2)

GasFee03.metric("ETHEREUM", "$1,465.16")
GasFee04.metric("", "")

cost_analysis = pd.read_csv("sabot_cost_analysis.csv")
st.dataframe(cost_analysis)

