# Imports
import streamlit as st
from pathlib import Path
from st_functions import st_button, load_css
from PIL import Image

st.set_page_config(layout="wide", page_title="Sabot")
st.header("THE TEAM")

st.markdown("---")

col1, col2, col3, col4, col5 = st.columns(5)
iconsize = 20

with col1:
    st.header("Quintin Bland")
    st.image("./images/Team/Quintin_Bland_bw.png")
    st_button("linkedin", "https://www.linkedin.com/in/quintin-bland-a2b94310b/", "LinkedIn", iconsize)

with col2:
    st.header("Kevin Corstorphine")
    st.image("./images/Team/Kevin_Corstorphine_bw.png")
    st_button("linkedin", "https://www.linkedin.com/in/kevin-corstorphine-9020a7113/", "LinkedIn", iconsize)

with col3:
    st.header("John Gruenewald")
    st.image("./images/Team/John_Gruenewald_bw.png")
    st_button("linkedin", "https://www.linkedin.com/in/jhgruenewald/", "LinkedIn", iconsize)

with col4:
    st.header("Martin Smith")
    st.image("./images/Team/Martin_Smith_bw.png")
    st_button("linkedin", "https://www.linkedin.com/in/smithmartinp/", "LinkedIn", iconsize)

with col5:
    st.header("Yanick Wilisky")
    st.image("./images/Team/Yanick_Wilisky_bw.png")
    st_button("linkedin", "https://www.linkedin.com/in/yanickwilisky/", "LinkedIn", iconsize)


