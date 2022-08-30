import os
import requests
import json
import streamlit as st
from bip44 import Wallet
from web3 import Web3, Account
from dotenv import load_dotenv
from mnemonic import Mnemonic
from pathlib import Path
from st_functions import st_button, load_css

load_dotenv()

@st.cache
def get_addresses():
    addresses = {
        "usdt_address": os.getenv("USDT_ADDRESS"),
        "susd_address": os.getenv("SUSD_ADDRESS"),
        "sabot_staking_contract_address": os.getenv("SABOT_STAKING_BASE_CONTRACT_ADDRESS"),
        "clog_address": os.getenv("CLOG_CONTRACT_ADDRESS"),
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
    with open(Path(os.getenv("SABOT_STAKING_ABI_FILE")),'r') as abi_file:
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
    clog_contract = get_w3().eth.contract(address = clog_address, abi = clog_abi)
    usdt_abi = get_usdt_abi()
    usdt_address = get_addresses()["usdt_address"]
    usdt_contract = get_w3().eth.contract(address=usdt_address, abi=usdt_abi)
    sabot_staking_abi = get_sabot_staking_abi()
    sabot_staking_address = get_addresses()["sabot_staking_contract_address"]
    sabot_staking_contract = get_w3().eth.contract(address=sabot_staking_address, abi=sabot_staking_abi)
    account = st.session_state["account"]


    try:
        # 1st call to usdt decimals
        usdt_decimals = usdt_contract.functions.decimals().call()
        usdt_in_decimals = int(amount * (10**usdt_decimals))
        print(f"When you stake {amount} USDT with decimals of {usdt_decimals} it becomes: {usdt_in_decimals}")
        
        # 2nd call to usdt approve function. Getting transaction receipt
        tx_hash = usdt_contract.functions.approve(sabot_staking_address, usdt_in_decimals).transact({'from': account.address , 'gas': 3000000})
        receipt = get_w3().eth.getTransactionReceipt(tx_hash)

        approval_event = usdt_contract.events.Approval().processReceipt(receipt)[0]
        if approval_event is not None and "event" in approval_event and approval_event["event"]=="Approval":
            st.write(f"Approval of {usdt_in_decimals}")
            # print(approval_event)
        
            # call staking method, pass in approved amount and USDT contract
            tx_hash = sabot_staking_contract.functions.stakeTokens(usdt_in_decimals, usdt_address).transact({'from': account.address , 'gas': 30000000})
            print(tx_hash)
            receipt = get_w3().eth.getTransactionReceipt(tx_hash)

            # After approval, issue CLOG 

            stake_event = sabot_staking_contract.events.Staked().processReceipt(receipt)[0]
            print(f'Stake event: {stake_event}')
            print(f'Transaction receipt {receipt}')
            if stake_event is not None and "event" in stake_event and stake_event["event"] =="Staked":
                st.write("You've successfully staked USDT")
            else:
                st.write("Stake failed.")
        else:
            st.write("Approval failed")

    except ValueError as err:
        print(err)


# ************* Streamlit View Below ***********************

st.set_page_config(layout="wide")

# TODO: Create Variable for sabot logo to use on each page
with st.container():
    logo_col, title_col = st.columns([25,100])
    with logo_col:
        st.image("images\sabot_logo.png", width=150)
    with title_col:
        st.markdown('<div><span style="font-size: 56px; font-weight: 700; position: relative; top: 20px;">SaBot</span></div>', 
        unsafe_allow_html=True)

sidebar_logo = st.sidebar.image("images\sabot_logo.png", width=75) 

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Intro", "Architechture", "Staking", "Arbitrage Trading", "Next Steps"])

with tab1:
    with st.container():
        st.header("Intro")
        st.markdown("---")
        st.subheader("Project Outline")
        st.write("""
        The SabotStaking Pool is a configurable fit for purpose defi pool aimed at accelerating the implementation of automated cryptocurrency arbitrage trading strategies.
        The solution consists of a set of coordinated web3 applications and smart contracts that are designed to 
        * secure participant assets
        * prevent risk of fraud, rug pulls and other nefarious actions
        * minimize transaction costs through on-chain trading
        * scale to support the demands of large defi solutions""")

with tab2:
    with st.container():
        st.header("Architechture")
        # diagrams
        # st.image()
        # markdown table with costs
        # st.markdown(pd.DataFrame{})

with tab3:
    initial_balance_usdt = 0
    initial_balance_clog = 0
    clog_abi = get_clog_abi()
    clog_address = get_addresses()["clog_address"]
    clog_contract = get_w3().eth.contract(address = clog_address, abi = clog_abi)
    usdt_abi = get_usdt_abi()
    usdt_address = get_addresses()["usdt_address"]
    usdt_contract = get_w3().eth.contract(address=usdt_address, abi=usdt_abi)
    with st.container():
        st.header("Staking")
        st.subheader("Welcome! Please connect your wallet to begin")
        left_col, right_col = st.columns([5,1])
        with left_col:
        # connect wallet button
        # create 2 columns
        # right column: st.header(wallet address)
        # below header show usdt balance
        # below show clog balance
        # goal: show balances before and after staking
            user_wallet = st.text_input("Please enter your wallet address")
            if st.button("Connect Wallet"):
                if "account" in st.session_state:
                    del st.session_state["account"]
                account = generate_account(user_wallet)

                st.write("Connecting...") # displayed when button is clicked

                if account is None:
                    st.write(f"Unable to connect to {account}.")
                else:
                    st.write("Connected successfully")               
                    st.session_state["account"] = account
                    usdt_balance = usdt_contract.functions.balanceOf(account.address).call()
                    clog_balance = clog_contract.functions.balanceOf(account.address).call()
                    with right_col:
                        right_col.metric("USDT balance before stake", usdt_balance / 10**18)
                        right_col.metric("Clog balance before stake", clog_balance / 10**18)


            if "account" in st.session_state:
                with st.container():
                    usdt_stake_amount = st.text_input("Enter amount of USDT to stake")
                    if st.button("Stake"):
                        stake(float(usdt_stake_amount))
                        usdt_balance = usdt_contract.functions.balanceOf(st.session_state["account"].address).call()
                        clog_balance = clog_contract.functions.balanceOf(st.session_state["account"].address).call()
                        right_col.metric("USDT balance after stake", usdt_balance / 10**18)
                        right_col.metric("Clog balance after stake", clog_balance / 10**18)

with tab4:
    with st.container():
        st.header("Arbitrage Trading")
        

with tab5:
    with st.container():
        st.header("Next Steps")

st.markdown("---")