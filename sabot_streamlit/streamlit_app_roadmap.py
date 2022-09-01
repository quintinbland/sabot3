# Imports
import streamlit as st
from pathlib import Path
from st_functions import st_button, load_css
from PIL import Image

st.set_page_config(layout="wide", page_title="Sabot")

st.title("Evolution of SaBot")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='text-align: center; color: light grey;'>PROJECT 1 | StableOps</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: light grey;'>Quantitative anaylsis demonstrating that arbitrage trading of stable coin volatility could be profitable.</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.image("./images/sabot_project_01_720.png")

with col2:
    st.markdown("<h3 style='text-align: center; color: light grey;'>PROJECT 2 | SaBot</h3>", unsafe_allow_html=True)
    st.markdown("Demonstrated that ML models could be leveraged to implement a successful automated arbitrage trading strategy.")
    st.markdown("---")
    st.image("./images/sabot_project_02_720.png")

st.markdown("---")
st.markdown("<h3 style='text-align: center; color: light grey;'>PROJECT 3 | SaBot Staking Pool</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: light grey;'>Leveraging the blockchain to realize a secure, low cost and scalable solution for stable coin arbitrage trading.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: light grey;'>Integrated web3 applications to work with SaBot.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: light grey;'>Creating a trustless experience for participants to interact with the bot on-chain.</p>", unsafe_allow_html=True)
st.text(" ")
st.text(" ")
st.text(" ")
st.markdown("<h3 style='text-align: center; color: light grey;'>Benefits of Using Blockchain Technology</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: light grey;'>Ability to directly use low cost DEXs with appropriate liquidity.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: light grey;'>Ability to implement a scalable DeFi solution that allows crypto users to securely pool funds in a trustless manner.</p>", unsafe_allow_html=True)
st.markdown("<li style='text-align: center; color: light grey;'>Auditable contract code.</li>", unsafe_allow_html=True)
st.markdown("<li style='text-align: center; color: light grey;'>Auditable transaction.</li>", unsafe_allow_html=True)
st.markdown("<li style='text-align: center; color: light grey;'>Full transparency.</li>", unsafe_allow_html=True)
st.markdown("<li style='text-align: center; color: light grey;'>Uncensorable.</li>", unsafe_allow_html=True)
st.markdown("<li style='text-align: center; color: light grey;'>No middleman.</li>", unsafe_allow_html=True)
st.markdown("<li style='text-align: center; color: light grey;'>Utility token to manage participant ownership stake.</li>", unsafe_allow_html=True)



