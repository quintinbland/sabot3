import os
from time import sleep
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

def get_contract_filter():
    if 'contract_filter' not in st.session_state:
        sabot_staking_abi = get_sabot_staking_abi()
        sabot_staking_address = get_addresses()["sabot_staking_contract_address"]
        sabot_staking_contract = get_w3().eth.contract(address=sabot_staking_address, abi=sabot_staking_abi)
        contract_filter = get_w3().eth.filter({"address": sabot_staking_address})
        st.session_state['contract'] = sabot_staking_contract
        st.session_state['contract_filter'] = contract_filter
    return st.session_state['contract'],st.session_state['contract_filter']

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
    # clog_abi = get_clog_abi()
    # clog_address = get_addresses()["clog_address"]
    # clog_contract = get_w3().eth.contract(address = clog_address, abi = clog_abi)
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
            # st.write(f"Approval of {usdt_in_decimals}")
            # print(approval_event)
        
            # call staking method, pass in approved amount and USDT contract
            tx_hash = sabot_staking_contract.functions.stakeTokens(usdt_in_decimals, usdt_address).transact({'from': account.address , 'gas': 30000000})
            print(tx_hash)
            receipt = get_w3().eth.getTransactionReceipt(tx_hash)

            # After approval, issue CLOG 

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
def get_current_block():
    return get_w3().eth.get_block('latest')['number']

def handle_event(contract,event_raw):
    # @TODO: get these from contracts
    utility_decimals = 18 # clogs is 18 decimals
    base_decimals = 6 # usdt is 6 decimals
    target_decimals = 18 # susd is 18 decimals

    receipt = get_w3().eth.getTransactionReceipt(event_raw['transactionHash'])
    swapped_event = contract.events.Swapped().processReceipt(receipt)
    minted_event = contract.events.Minted().processReceipt(receipt)
    burned_event = contract.events.Burned().processReceipt(receipt)
    staked_event = contract.events.Staked().processReceipt(receipt)  
    unstaked_event = contract.events.Unstaked().processReceipt(receipt)  
    exchange_rate_event = contract.events.ExchangeRate().processReceipt(receipt)  

    if swapped_event is not None and len(swapped_event)>0 and 'event' in swapped_event[0]:
        if 'args' in swapped_event[0]:
            event_record = make_event_record('Swapped',swapped_event[0]['args'])
            st.session_state['clog_supply'] = event_record['utilityTokenTotalSupply']/10**utility_decimals
            if model_profit:
                st.session_state['balanceOfBaseToken'] = st.session_state['balanceOfBaseToken']*1.015
                event_record['balanceOfBaseToken'] = st.session_state['balanceOfBaseToken']
            else:
                st.session_state['balanceOfBaseToken'] = event_record['balanceOfBaseToken']
            st.session_state['portfolio_value'] = event_record['balanceOfBaseToken']/10**base_decimals + event_record['balanceOfTargetToken']/10**target_decimals
            st.session_state['clog_price']= st.session_state['portfolio_value']/st.session_state['clog_supply'] 
            event_record['clog_price']=st.session_state['clog_price']
            push(event_record)
    if minted_event is not None and len(minted_event)>0 and 'event' in minted_event[0]:
        if 'args' in minted_event[0]:
            event_record = make_event_record('Minted',minted_event[0]['args'])
            push(event_record)
    if burned_event is not None and len(burned_event)>0 and 'event' in burned_event[0]:
        if 'args' in burned_event[0]:
            event_record = make_event_record('Burned',burned_event[0]['args'])
            push(event_record)
    if staked_event is not None and len(staked_event)>0 and 'event' in staked_event[0]:
        if 'args' in staked_event[0]:
            event_record = make_event_record('Staked',staked_event[0]['args'])
            push(event_record)
    if unstaked_event is not None and len(unstaked_event)>0 and 'event' in unstaked_event[0]:
        if 'args' in unstaked_event[0]:
            event_record = make_event_record('Unstaked',unstaked_event[0]['args'])
            push(event_record)
    if exchange_rate_event is not None and len(exchange_rate_event)>0 and 'event' in exchange_rate_event[0]:
        if 'args' in exchange_rate_event[0]:
            event_record = make_event_record('ExchangeRate',exchange_rate_event[0]['args'])
            push(event_record)

def push(event):
    # print(f"pushing {event}")
    if 'data_df' in st.session_state:
        st.session_state['data_df']=pd.concat([st.session_state['data_df'],pd.DataFrame([event])])
    else:
        st.session_state['data_df']=pd.DataFrame([event])

def make_event_record(type,args):
    event_record = {
        'time':datetime.now().timestamp(),
        'type':type,
        'sellToken':None,
        'sellTokenAmount':None,
        'buyToken':None,
        'buyTokenAmount':None,
        'utilityToken':None,
        'utilityTokenAmount':None,
        'utilityTokenTotalSupply':None,
        'balanceOfBaseToken':None,
        'balanceOfTargetToken':None,
        'owner':None,
        'exchangeRate':None
    }
    if args is not None:
        for key,value in args.items():
            event_record[key]=value
    return event_record

def get_logs():
    # print('get event logs')
    contract, contract_filter=get_contract_filter()
    logs = get_w3().eth.getFilterChanges(contract_filter.filter_id)
    # print(logs)
    if len(logs)>0:
        event = logs[0]
        handle_event(contract,event)

def get_portfolio_value():
    if 'portfolio_value' in st.session_state:
        return f"${st.session_state['portfolio_value']:.4f}"
    else:
        return ''

def get_clog_price():
    if 'clog_price' in st.session_state:
        return f"${st.session_state['clog_price']:.2f}"
    else:
        return ''

def get_clog_supply():
    if 'clog_supply' in st.session_state :
        return f"{st.session_state['clog_supply']}"
    else:
        return ''

def get_data():
    # print('get data')
    if 'data_df' in st.session_state:
        return st.session_state['data_df']
    else:
        return None
# ************* Streamlit View Below ***********************

st.set_page_config(layout="wide", page_title="Sabot")


# TODO: Create Variable for sabot logo to use on each page
with st.container():
    logo_col, title_col = st.columns([10,90])
    with logo_col:
        st.image("sabot_streamlit/images/sabot_logo.png", width=150)
    with title_col:
        st.markdown('<div><span style="font-size: 56px; font-weight: 700; position: relative; top: 20px;">SaBot</span></div>', 
        unsafe_allow_html=True)

# sidebar_logo = st.sidebar.image("images\sabot_logo.png", width=75) 

roadmap, solution, tokenomics, staking, automated_trading, whats_next, devs = st.tabs(["Roadmap", "Solution", "Tokenomics", "Staking", "Automated Trading", "What's Next","Developers"])

with roadmap:
    # implement columns for each container - yanick has the vision
    with st.container():
        st.title("Evolution of SaBot")
        st.header("Project 1: StableOps")
        st.markdown("---")
        st.write("Quantitative anaylsis demonstrating that arbitrage trading of stable coin volatility could be profitable.")
        st.write("image of volatile stable coins. 'overlapping coin prices' ")
        st.write("sharpe ratio image")

    with st.container():
        st.header("Project 2: SaBot")
        st.markdown("---")
        st.write("Demonstrated that ML models could be leveraged to implement a successful automated arbitrage trading strategy.")
        st.write("pickle rick bot, consistent positive return images")

    with st.container():
        st.header("Project 3: SaBot Staking Pool")
        st.markdown("---")
        st.write("Leveraging the blockchain to realize a secure, low cost and scalable solution for stable coin arbitrage trading.")
        st.write("Why a pool? need sufficient volume to combat high fees. ")
        st.write("Integrated web3 applications to work with SaBot. Creating a trustless experience for participants to interact with the bot on-chain")
        st.write("Vitalik would be proud")
        st.write("DeFi and Low Cost, access to a 4bps trading platform")

        st.subheader("Benefits of using blockchain: ")
        st.markdown("""
        * Ability to directly use low cost DEXs with appropriate liquidity.
        * Ability to implement a scalable DeFi solution that allows crypto users to securely pool funds in a trustless manner.
            * Auditable contract code
            * Auditable transaction
            * Full transparency
            * Uncensorable
            * No middleman
            * Utility token to manage participant ownership stake
        """)


with solution:
    with st.container():
        st.title("Solution")
        # diagrams
        st.image("sabot_streamlit/images/sabot-solution.png")
        st.image("sabot_streamlit/images/sabotstaking-class-diagram.png")
        st.image("sabot_streamlit/images/clog-class-diagram.png")
        st.markdown("""
        ### Cost Analysis
An exploration of costs was conducted.  At the time of the analysis

* gas fee = 10 gwei
* 1 eth = $1,465.16

| Transaction | Version | Gas | gwei | cost $(USD) |
|-------------|---------|-----|-----|------| 
| Deploy Test Assets |   -  | 4968102 | 49681020 | 126.92 |
| Deploy SabotStaking Assets | non-proxy | 6784487 | 67844870 | 173.33 |
| Deploy SabotStaking Assets | proxy | 9069888 | 90698880 | 231.72 |
| Directly call Curve pool exchange method |  -  | 25457 | 254570 | 0.65037 |
| Bot calling swap method | non-proxy | 51902 | 519020 | 1.3260 |
| Bot calling swap method | proxy | 68661 | 686610 | 1.7541 |
| ERC20 approval for staking |  -  | 46179 | 461790 | 1.1798 |
| Staking | non-proxy | 130105 | 1301050 | 3.3239 |
| Staking | proxy | 132993 | 1329930 | 3.3239 | 3.3977 |
""")


with tokenomics:
    with st.container():
        st.title("SaBot Tokenomics")
        st.markdown("""
        #### Clog: ERC20 Utility Token
        ####  Purpose: To fund the automated trading bot
        #### Initial Exchange Rate: 1 USDT = 1 CLOG
        * Subsequent staking will be at prevailing clog price.
        #### Clog Price 
        * As the porfolio value increases, the price of the clog upon staking will adjust to reflect change in portfolio value
        * Clog Price = (Portfolio Value / Total Clog Supply)
        """)

with staking:
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

                # right_col.metric("Wallet Address:")

                if account is None:
                    st.write(f"Unable to connect to {account}.")
                else:
                    st.write("Connected successfully")               
                    st.session_state["account"] = account
                    usdt_balance = usdt_contract.functions.balanceOf(account.address).call()
                    clog_balance = clog_contract.functions.balanceOf(account.address).call()
                    with right_col:
                        right_col.metric("USDT balance", usdt_balance / 10**18)
                        right_col.metric("Clog balance", clog_balance / 10**18)


            if "account" in st.session_state:
                with st.container():
                    usdt_stake_amount = st.text_input("Enter amount of USDT to stake")
                    if st.button("Stake"):
                        stake(float(usdt_stake_amount))
                        usdt_balance = usdt_contract.functions.balanceOf(st.session_state["account"].address).call()
                        clog_balance = clog_contract.functions.balanceOf(st.session_state["account"].address).call()
                        right_col.metric("USDT balance after stake", usdt_balance / 10**18)
                        right_col.metric("Clog balance after stake", clog_balance / 10**18)


with whats_next:
    with st.container():
        st.title("What's Next")
        st.markdown("""
        * Create governance token with rewards
        * Multi-sig wallet
        * Unstaking / burning
        * DAO with proposal process and voting
        * Deploying on test chain.
        * Refactoring contracts to lower transaction costs.
        * Improve web3 UI.
        * Staking pool with other crypto pairs.
        * Broaden support for other liquidity pools
        * Returning profits to stakeholders via MEV
        """)


with devs:
    with st.container():
        st.header("Developers")
        st.subheader("Connect with the team!")
        load_css()

        col1, col2, col3 = st.columns(3)

        iconsize = 20

        # add in links for github/linked-in profiles 
        st.subheader("Quintin Bland")
        st_button("linkedin", "https://www.linkedin.com/in/quintin-bland-a2b94310b/", "Follow me on LinkedIn", iconsize)
        st.subheader("Kevin Corstorphine")
        st_button("linkedin", "https://www.linkedin.com/in/kevin-corstorphine-9020a7113/", "Follow me on LinkedIn", iconsize)
        st.subheader("John Gruenewald")
        st_button("linkedin", "https://www.linkedin.com/in/jhgruenewald/", "Follow me on LinkedIn", iconsize)
        st.subheader("Martin Smith")
        st_button("linkedin", "https://www.linkedin.com/in/smithmartinp/", "Follow me on LinkedIn", iconsize)
        st.subheader("Yanick Wilisky")
        st_button("linkedin", "https://www.linkedin.com/in/yanickwilisky/", "Follow me on LinkedIn", iconsize)

st.markdown("---")

with automated_trading:    
    with open('sabot_streamlit/style2.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    done = False
    st.header("Sabot Dashboard")
    st.markdown("Bot is now funded, lets trade!")
    model_profit = st.checkbox("Model Profit")

    with st.empty():
        while not done:
            get_logs()
            with st.container():            
                with st.container():            
                    a1, a2, a3, a4 = st.columns(4)
                    a1.metric("CLOG Price", get_clog_price())
                    a2.metric("CLOGs in circulation", get_clog_supply())
                    a3.metric("Portfolio Value", get_portfolio_value())
                    a4.metric("Current Block", get_current_block())

                with st.container():    
                    df = get_data()
                    if df is not None:
                        # tab1, tab2, tab3 = st.tabs(["24hrs", "7days", "30days"])
                        tab1, tab2 = st.tabs(["staking pool events","clog price" ])
                        with tab1:
                            st.markdown("Staking Pool Events")
                            st.write(df)

                        with tab2:
                            swapped_df = df.loc[df['type']=='Swapped'][['time','clog_price']]
                            st.markdown("### CLOG Price Chart (CLOG/USD)")
                            st.line_chart(.to_numpy())      
                            # st.line_chart(df['clog_price'].to_numpy())      

                        # with tab3:
                        #     st.markdown("### CLOG Price Chart (CLOG/USD)")
                        #     st.area_chart(np.random.randn(150, 1))


                    # st.write(get_data())

                # data = pd.read_csv("data/sabot_events.log")

                # chart_data = pd.DataFrame(data, columns=["time", "sellTokenAmount"])
                # chart_data_clean = chart_data.dropna()
                # st.area_chart(chart_data_clean)


            sleep(3)
        
