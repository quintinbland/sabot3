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
from time import sleep
from datetime import datetime


load_dotenv()

@st.cache
def get_addresses():
    addresses = {
        "usdt_address": os.getenv("USDT_ADDRESS"),
        "susd_address": os.getenv("SUSD_ADDRESS"),
        "sabot_staking_contract_address": os.getenv("SABOT_SWAP_ADDRESS"),
        "sabotstaking_address": os.getenv("SABOT_SWAP_ADDRESS"),
        "clog_address": os.getenv("CLOG_ADDRESS"),
    }
    return addresses

def get_w3():
    if "w3" not in st.session_state:
        st.session_state["w3"] = Web3(Web3.HTTPProvider(os.getenv("GANACHE_URL")))
    return st.session_state["w3"]



def mnemonic_generator(address):
    """
    Checks .env file of the parent directory for variable named mnemonic ("MNEMONIC").
    If file is empty, mnemonic is created with specified strength (128-bit or 256-bit).
    Stores newly created mnemonic phrase in .env file.
    
    Input Parameters:
    
    strength (int) : Strength of seed mnemonic phrase implementing the 2,048 word
                     list of BIP-39.
                     Default strength is equal to 128.
                     For 12-word phrases, use 128.  For 24-word phrases, use 256.  
    language (str) : Default language is 'english'.  For complete list of options,
                     visit: https://github.com/bitcoin/bips/tree/master/bip-0039
    
    Returns:
    
    mnemonic (str) : A string with the BIP-39 mnemonic of specified strength.
    
    """
    mnemonic = os.getenv(address)
    return mnemonic


def generate_account(address):
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    # Fetch mnemonic from environment variable.
    mnemonic = mnemonic_generator(address)
    if mnemonic is None:
        return None

    # Create Wallet Object
    wallet = Wallet(mnemonic)

    # Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")

    # Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)

    return account



@st.cache
def get_sabot_staking_abi():
    abi = None
    with open(Path(os.getenv("SABOTSTAKING_ABI")),'r') as abi_file:
        abi = json.load(abi_file) 
        st.session_state["sabot_staking_abi"] = abi
    return st.session_state["sabot_staking_abi"]
    return abi

@st.cache
def get_clog_abi():
    abi = None
    with open(Path(os.getenv("CLOG_ABI")),'r') as abi_file:
        abi = json.load(abi_file)
        st.session_state["clog_abi"] = abi
    return st.session_state["clog_abi"]

@st.cache
def get_usdt_abi():
    if "usdt_abi" not in st.session_state:
        with open(Path(os.environ["USDT_ABI"]),'r') as abi_file:
            abi = json.load(abi_file)
            # print(abi)
            st.session_state["usdt_abi"] = abi
    return st.session_state["usdt_abi"]

def stake(amount):
    clog_abi = get_clog_abi()
    clog_address = get_addresses()["clog_address"]
    print(f"clog_address={clog_address}")
    clog_contract = get_w3().eth.contract(address = clog_address, abi = clog_abi)
    usdt_abi = get_usdt_abi()
    usdt_address = get_addresses()["usdt_address"]
    usdt_contract = get_w3().eth.contract(address=usdt_address, abi=usdt_abi)
    print(f"usdt_address={usdt_address}")
    sabot_staking_abi = get_sabot_staking_abi()
    sabot_staking_address = get_addresses()["sabot_staking_contract_address"]
    sabot_staking_contract = get_w3().eth.contract(address=sabot_staking_address, abi=sabot_staking_abi)
    print(f"sabot_staking_address={sabot_staking_address}")
    # account = st.session_state["account"]
    # print(f"account={account.address}")

    try:
        # 1st call to usdt decimals
        usdt_decimals = usdt_contract.functions.decimals().call()
        usdt_in_decimals = int(amount * (10**usdt_decimals))
        print(f"When you stake {amount} USDT with decimals of {usdt_decimals} it becomes: {usdt_in_decimals}")
        
        # 2nd call to usdt approve function. Getting transaction receipt
        wallet_address = st.session_state['connected_address']
        tx_hash = usdt_contract.functions.approve(sabot_staking_address, usdt_in_decimals).transact({'from': wallet_address , 'gas': 3000000})
        receipt = get_w3().eth.getTransactionReceipt(tx_hash)
    
        approval_event = usdt_contract.events.Approval().processReceipt(receipt)[0]
        # block_number = sabot_staking_contract.events.Staked().processReceipt(receipt)[1]
        if approval_event is not None and "event" in approval_event and approval_event["event"]=="Approval":
            st.write(f"{sabot_staking_address} approved for {usdt_in_decimals} USDT")
            # print(approval_event)
        
            # call staking method, pass in approved amount and USDT contract
            tx_hash = sabot_staking_contract.functions.stakeTokens(usdt_in_decimals, usdt_address).transact({'from': wallet_address , 'gas': 30000000})
            print(tx_hash)
            receipt = get_w3().eth.getTransactionReceipt(tx_hash)

            # After approval, issue CLOG 
            # block_number = sabot_staking_contract.events.Staked().processReceipt(receipt)[1]
            stake_event = sabot_staking_contract.events.Staked().processReceipt(receipt)[0]
            print(f'Stake event: {stake_event}')
            if stake_event is not None and "event" in stake_event and stake_event["event"] =="Staked":
                st.write("Stake successful")
            else:
                st.write("Stake failed.")
        else:
            st.write("Approval failed")

    except ValueError as err:
        print(err)


st.session_state['model_profit']=False


def get_df():
    block_number = get_w3().eth.get_block('latest')['number']
    # print(block_number)
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
    clog_decimals=18
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
        portfolio_value = float(latest['balanceOfBaseToken'])/10**usdt_decimals + float(latest['balanceOfTargetToken'])/10**susd_decimals
        st.session_state['portfolio_value']=portfolio_value
        print(f"latest['utilityTokenTotalSupply']={float(latest['utilityTokenTotalSupply'])}. type:{type(float(latest['utilityTokenTotalSupply']))}")
        print(f"portfolio_value={portfolio_value}. type:{type(portfolio_value)}")
    clog_price=0
    if float(latest['utilityTokenTotalSupply']) != 0.0:
        clog_price=portfolio_value / (float(latest['utilityTokenTotalSupply'])/10**clog_decimals)
    return clog_price,float(latest['utilityTokenTotalSupply'])/10**clog_decimals,portfolio_value,latest['block_number']

df = get_df()

# ************* Streamlit View Below ***********************

st.set_page_config(layout="wide", page_title="Sabot")


with st.container():
    logo_col, title_col = st.columns([10,90])
    with logo_col:
        st.image("images/sabot_logo.png", width=150)
    with title_col:
        st.markdown('<div><span style="font-size: 56px; font-weight: 700; position: relative; top: 20px;">SaBot Staking</span></div>', 
        unsafe_allow_html=True)


roadmap, solution, tokenomics, staking, dashboard, whats_next, devs = st.tabs(["Roadmap", "Solution", "Tokenomics", "Staking", "Dashboard", "What's Next","Team"])

with roadmap:
    with st.container():
        st.title("Evolution of SaBot")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: left; color: light grey;'>PROJECT 1 | StableOps</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: left; color: light grey;'>Quantitative anaylsis demonstrating that arbitrage trading of stable coin volatility could be profitable.</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.image("./images/sabot_project_01_720.png")

    with col2:
        st.markdown("<h3 style='text-align: left; color: light grey;'>PROJECT 2 | SaBot</h3>", unsafe_allow_html=True)
        st.markdown("Demonstrated that ML models could be leveraged to implement a successful automated arbitrage trading strategy.")
        st.markdown("---")
        st.image("./images/sabot_project_02_720.png")

    st.markdown("---")
    st.markdown("<h3 style='text-align: left; color: light grey;'>PROJECT 3 | SaBot Staking Pool</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: light grey;'>Leveraging the blockchain to realize a secure, low cost and scalable solution for stable coin arbitrage trading.</p>", unsafe_allow_html=True)
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.markdown("<h3 style='text-align: left; color: light grey;'>Benefits of Using Blockchain Technology</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: light grey;'>Ability to directly use low cost DEXs with appropriate liquidity.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; color: light grey;'>Ability to implement a scalable DeFi solution that allows crypto users to securely pool funds in a trustless manner.</p>", unsafe_allow_html=True)
    st.markdown("<li style='text-align: left; color: light grey;'>Auditable contract code.</li>", unsafe_allow_html=True)
    st.markdown("<li style='text-align: left; color: light grey;'>Auditable transaction.</li>", unsafe_allow_html=True)
    st.markdown("<li style='text-align: left; color: light grey;'>Full transparency.</li>", unsafe_allow_html=True)
    st.markdown("<li style='text-align: left; color: light grey;'>Uncensorable.</li>", unsafe_allow_html=True)
    st.markdown("<li style='text-align: left; color: light grey;'>No middleman.</li>", unsafe_allow_html=True)
    st.markdown("<li style='text-align: left; color: light grey;'>Utility token to manage participant ownership stake.</li>", unsafe_allow_html=True)



with solution:
    with st.container():
        st.title("Solution")
        col_sol1, col_sol2 = st.columns(2)

        with col_sol1:
            st.header("Architecture")
            st.image("images/sabot_architecture.png")

        with col_sol2:
            st.header("Class Diagram")
            st.image("images/sabot_class_diagram2.png")

        st.markdown("---")

        st.markdown("<h2 style='text-align: left; color: light grey;'>Cost Analysis</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: left; color: light grey;'>Exploration of Costs Conducted at the Time of the Analysis.</p>", unsafe_allow_html=True)

        GasFee01, GasFee02 = st.columns(2)

        GasFee01.metric("GAS FEE", "10 gwei")
        GasFee02.metric("","")

        GasFee03, GasFee04 = st.columns(2)

        GasFee03.metric("ETHEREUM", "$1,465.16")
        GasFee04.metric("", "")

        cost_analysis = pd.read_csv("sabot_streamlit/sabot_cost_analysis.csv")
        st.dataframe(cost_analysis)


with tokenomics:
    with st.container():
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

with staking:
    clog_abi = get_clog_abi()
    clog_address = get_addresses()["clog_address"]
    clog_contract = get_w3().eth.contract(address = clog_address, abi = clog_abi)
    usdt_abi = get_usdt_abi()
    usdt_address = get_addresses()["usdt_address"]
    usdt_contract = get_w3().eth.contract(address=usdt_address, abi=usdt_abi)
    sabot_staking_abi = get_sabot_staking_abi()
    sabot_staking_address = get_addresses()["sabot_staking_contract_address"]
    sabot_staking_contract = get_w3().eth.contract(address=sabot_staking_address, abi=sabot_staking_abi)
    # usdt_decimals = usdt_contract.functions.decimals().call()
    # usdt_in_decimals = int(amount * (10**usdt_decimals))
    # tx_hash = usdt_contract.functions.approve(sabot_staking_address, usdt_in_decimals).transact({'from': account.address , 'gas': 3000000})
    # receipt = get_w3().eth.getTransactionReceipt(tx_hash)
    # block_number = sabot_staking_contract.events.Staked().processReceipt(receipt)[0]['blockNumber']

    with st.container():
        st.header("Staking")
        st.subheader("Welcome! Please connect your wallet to begin")
        # left_col, right_col = st.columns([5,1])
        # with left_col:
        # connect wallet button
        # create 2 columns
        # right column: st.header(wallet address)
        # below header show usdt balance
        # below show clog balance
        # goal: show balances before and after staking
        user_wallet = st.text_input("Please enter your wallet address")
        if st.button("Connect Wallet"):
            account = generate_account(user_wallet)
            if account is None:
                st.write(f"Unable to connect to {account}.  Please select a different address")
            else:
                st.session_state['connected']=True
                st.session_state['connected_address']=user_wallet
                # st.write("Connected successfully")               
            
        if 'connected' in st.session_state:  
            with st.container():
                usdt_balance = usdt_contract.functions.balanceOf(user_wallet).call()
                clog_balance = clog_contract.functions.balanceOf(user_wallet).call()
                c1,c2 = st.columns([50,50])
                c2.subheader("Before Stake")
                c2.metric(f"Connected wallet: ", user_wallet)
                c2.metric("USDT balance", usdt_balance / 10**6)
                c2.metric("Clog balance", clog_balance / 10**18)
                c2.markdown("---")

                with c1:
                    usdt_stake_amount = st.text_input("Enter amount of USDT to stake")
                    if st.button("Stake"):
                        print("here3")
                        stake(float(usdt_stake_amount))
                        usdt_balance = usdt_contract.functions.balanceOf(user_wallet).call()
                        clog_balance = clog_contract.functions.balanceOf(user_wallet).call()
                        c2.subheader("After Stake")
                        c2.metric(f"Connected wallet: ", user_wallet)
                        c2.metric("USDT balance", usdt_balance / 10**6)
                        c2.metric("Clog balance", clog_balance / 10**18)
                        c2.markdown("---")

        
with whats_next:
    with st.container():
        st.title("What's Next")
        st.markdown("""
        * Create governance token with rewards
        * Multi-sig wallet
        * Deploying on test chain.
        * Refactoring contracts to lower transaction costs.
        * Improve web3 UI.
        * Staking pool with other crypto pairs.
        * Broaden support for other trading platforms
        """)


with devs:
    with st.container():
        st.header("The Saboteurs")

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




with dashboard:
    with st.container():
        with open('sabot_streamlit/style2.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        st.session_state['model_profit']=False
        st.markdown(f'<img src="https://user-images.githubusercontent.com/9788128/187974396-613bf51e-edb7-4cac-963e-37b05ff8a10c.png" alt="live" width="60">', unsafe_allow_html=True)
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
                    a1.metric("CLOG Price", f"{clog_price:.2f}")
                    a2.metric("CLOGs in circulatiuon", f"{clog_supply:.2f}")
                    a3.metric("Total Portfolio Value", f"{portfolio_value:.2f}")
                    a4.metric("Current Block Number", block_number)
                    st.subheader("Latest Event")
                    st.dataframe(df.iloc[-1:][['block_number','type','sellToken','sellTokenAmount','buyToken']])
                sleep(2)