import os
import requests
import json
import streamlit as st
from bip44 import Wallet
from web3 import Account
from dotenv import load_dotenv
from mnemonic import Mnemonic
from pathlib import Path

def configure():
    load_dotenv()

def validateJSON(jsonData):
    try: 
        json.loads(jsonData)
    except ValueError as err:
        return False
    return True  

def mnemonic_generator(address, strength=128,
                       language='english'):
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
    load_dotenv()
    mnemonic = os.getenv(address)
    
    check_sum = {128:4,
                256:8}
    # Use an if-statement to check if the mnemonic variable is None
    if((mnemonic == None) | (mnemonic=='')):
        mnemo = Mnemonic(language)
    
        mnemonic = mnemo.generate(strength)
        
        with open('.env','a') as f:
            f.write(f'MNEMONIC={mnemonic}')
        
        return mnemonic
    elif((11.0*len(mnemonic.split())-check_sum[strength])/strength != 1):
        return '''Provided MNEMONIC in .env file does not match specified strength. Check word count or strength(128 or 256).'''        
    else:
        return mnemonic


def generate_account(address, strength=256,
                    language='english',
                    ):
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    # Fetch mnemonic from environment variable.
    mnemonic = mnemonic_generator(address)

    # Create Wallet Object
    wallet = Wallet(mnemonic)

    # Derive Ethereum Private Key
    private, public = wallet.derive_account("eth")

    # Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)

    return account




# mnemonic = os.getenv("MNEMONIC")
# if mnemonic is None:
#     mnemo = Mnemonic("english")
#     mnemonic = mnemo.generate(strength=256)

# wallet = Wallet(mnemonic)

# private, public = wallet.derive_account("eth")

# account = Account.privateKeytoAccount(private)

# TODO: Create Variable for sabot logo to use on each page
with st.container():
    logo_col, title_col = st.columns([25,100])
    with logo_col:
        st.image("images\sabot_logo.png", width=150)
    with title_col:
        st.markdown('<div><span style="font-size: 56px; font-weight: 700; position: relative; top: 20px;">SaBot</span></div>', 
        unsafe_allow_html=True)

# need sabot logo .png/.jpg file if we use more than 1 page
st.sidebar.image("images\sabot_logo.png", width=75) 

def main():
    configure()
    st.markdown("---")
    st.subheader("Welcome! Please connect your wallet to begin")


if __name__ == '__main__':
    main()


# connect wallet button
user_wallet = st.text_input("Please enter your wallet address")

# Creating empty json dictionary
# wallet_info = {
#     "account address": "",
#     "mnemonic": "",
#     "public key": "",
#     "private key": ""}
# addresses = json.loads(wallet_info)

if st.button("Connect Wallet"):
    account = generate_account(user_wallet)

    st.write("Connecting...") # displayed when button is clicked

    st.write(account.address)

    # validate address with .json dictionary / .env file
    # stuck
    # function to validate address
    # validateJSON(user_wallet) 
    # if found, retrieve private key

    # return to original screen
    st.write("Wallet connected")


# add abi and contract address to .env file
# run method to 
st.subheader("Stake USDT for CLOG")

if st.button("Stake"):
    st.number_input("Choose amount of USDT to Stake", )




