import os
import streamlit as st
from st_functions import st_button, load_css
from PIL import Image


st.title("About")
st.subheader("""
The SabotStaking Pool is a configurable fit for purpose defi pool aimed at accelerating the implementation of automated cryptocurrency arbitrage trading strategies.
The solution consists of a set of coordinated web3 applications and smart contracts that are designed to:
* secure participant assets
* prevent risk of fraud, rug pulls and other nefarious actions
* minimize transaction costs through on-chain trading
* scale to support the demands of large defi solutions
""")

load_css()

col1, col2, col3 = st.columns(3)
# col2("./images/sabot_logo.png")



st.header("The Team")
st.subheader("")

iconsize = 20

# add in links for github/linked-in profiles 
st.subheader("Quintin Bland")
st_button("linkedin", "https://www.linkedin.com/in/quintin-bland-a2b94310b/", "Follow me on LinkedIn", iconsize)
st.subheader("Kevin Corstorphine")
st_button("linkedin", "https://www.linkedin.com/in/kevin-corstorphine-9020a7113/", "Follow me on LinkedIn", iconsize)
st.subheader("John Gruenwald")
st_button("linkedin", "https://www.linkedin.com/in/jhgruenewald/", "Follow me on LinkedIn", iconsize)
st.subheader("Martin Smith")
st_button("linkedin", "https://www.linkedin.com/in/smithmartinp/", "Follow me on LinkedIn", iconsize)
st.subheader("Yanick Wilisky")
st_button("linkedin", "https://www.linkedin.com/in/yanickwilisky/", "Follow me on LinkedIn", iconsize)