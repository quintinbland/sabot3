import os
import requests
import json
import streamlit as st
import numpy as np
import pandas as pd
from bip44 import Wallet
from web3 import Web3, Account
from dotenv import load_dotenv
from mnemonic import Mnemonic
from pathlib import Path
from st_functions import st_button, load_css
from PIL import Image
from datetime import datetime
from time import sleep

load_dotenv()
st.session_state['model_profit']=False
@st.cache
def get_addresses():
    addresses = {
            "usdt_address": os.getenv("USDT_ADDRESS"),
            "susd_address": os.getenv("SUSD_ADDRESS"),
            "clog_address": os.getenv("CLOG_ADDRESS"),
            "sabotstaking_address": os.getenv("SABOT_SWAP_ADDRESS"),
            "clog_address": os.getenv("CLOG_ADDRESS")}
    return addresses

def get_w3():
    if 'w3' not in st.session_state:
        st.session_state['w3']=Web3(Web3.HTTPProvider(os.getenv("GANACHE_URL")))
    return st.session_state['w3']

def get_df():
    block_number = get_w3().eth.get_block('latest')['number']
    print(block_number)
    usdt_decimals=6
    susd_decimals=18
    df = pd.read_csv('data/sabot_events.log')
    df = df[df['type']=='Swapped']
    df['block_number']=block_number
    return df 

def get_latest():
    latest = df.iloc[-1,:]
    usdt_decimals=6
    susd_decimals=18
    # portfolio_value = latest['balanceOfBaseToken']/10**usdt_decimals + latest['balanceOfTargetToken']/10**susd_decimals
    if 'model_profit' in st.session_state and st.session_state['model_profit']:
        portfolio_value=0
        if 'portfolio_value' in st.session_state:
            portfolio_value = st.session_state['portfolio_value']
        if portfolio_value == 0:
            portfolio_value = 1000
        portfolio_value = portfolio_value*1.015
        st.session_state['portfolio_value'] = portfolio_value
    else:
        portfolio_value = latest['balanceOfBaseToken']/10**usdt_decimals + latest['balanceOfTargetToken']/10**susd_decimals
        st.session_state['portfolio_value']=portfolio_value
    clog_price=portfolio_value / latest['utilityTokenTotalSupply']
    return clog_price,latest['utilityTokenTotalSupply'],portfolio_value,latest['block_number']
df = get_df()
# ************* Streamlit View Below ***********************

st.set_page_config(layout="wide", page_title="Sabot")

with st.container():
    logo_col, title_col = st.columns([25,100])
    with logo_col:
        st.image("sabot_streamlit/images/sabot_logo.png", width=150)
    with title_col:
        st.markdown('<div><span style="font-size: 56px; font-weight: 700; position: relative; top: 20px;">SaBot</span></div>', 
        unsafe_allow_html=True)


with st.container(): # mock for tab
    with open('sabot_streamlit/style2.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    st.session_state['model_profit']=False
    st.markdown("# Trading Dashboard")
    st.markdown("##### Bot is now funded, lets trade!")
    model_profit=st.checkbox("Model Profit")
    st.session_state['model_profit']=model_profit
    with st.empty():
        done = False
        loop = 100
        while not done:
            df = get_df()
            with st.container():
                a1, a2, a3, a4 = st.columns(4)
                clog_price,clog_supply,portfolio_value,block_number=get_latest()
                a1.metric("CLOG Price", clog_price)
                a2.metric("CLOGs in circulatiuon", clog_supply)
                a3.metric("Total Portfolio Value", portfolio_value)
                a4.metric("Current Block Number", block_number)
                st.dataframe(df.iloc[-1:][['block_number','type','sellToken','sellTokenAmount','buyToken','balanceOfBaseToken','balanceOfTargetToken']])
            sleep(3)
