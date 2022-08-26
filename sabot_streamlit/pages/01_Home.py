import os
import streamlit as st

st.set_page_config(layout="wide")

with st.container():
    logo_col, title_col = st.columns([5,95])
    with logo_col:
        st.image(os.environ['SABOT_LOGO'])
    with title_col:
        st.markdown('<div><span style="font-size: 56px; font-weight: 700; position: relative; top: -26px;">SaBot</span></div>', 
        unsafe_allow_html=True)

st.subheader("Home Page")