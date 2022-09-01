# BIP-44 Wallet Creation
################################################################################

# Implements the BIP-44 standards for multicurrency and multiaccount HD wallets.
# Store mnemonic in an .env file and a master account will be created implementing
# BIP-44. An arbitrary number (up to 2^{31} -1) of normal children addresses can be
# generated from parent address.

################################################################################
# Imports
import os
import sys
import time
import requests
from dotenv import load_dotenv
from bip44 import Wallet
from mnemonic import Mnemonic
import json

from web3 import Account
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3 import Web3

################################################################################
# Connect to network
def connect_RPC_server(env_path='./.env'):
    """
    Connect to the blockchain network.
    
    Input Parameters:
    rpc_server_address (str) : Address of RPC Server, i.e. 'HTTP://127.0.0.1:7545'
                               for Ganache
    
    Returns:
    w3 (obj): An instance of Web3 for the inputed network
    """
    try:
        load_dotenv(env_path)
        rpc_server_address = os.getenv("GANACHE_URL")
        return Web3(Web3.HTTPProvider(rpc_server_address))
    except:
        error_code=404
        return error_code
        

################################################################################
# Finding Mnemo
def mnemonic_generator(strength=128,
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
    mnemonic = os.getenv("MNEMONIC")
    
    check_sum = {128:4,
                256:8}
    # Use an if-statement to check if the mnemonic variable is None
    if((mnemonic == None) | (mnemonic=='')):
        mnemo = Mnemonic(language)
    
        mnemonic = mnemo.generate(strength)
        
        with open('.env','a') as f:
            f.write('\n')
            f.write(f'MNEMONIC="{mnemonic}"\n')
        
        return mnemonic
    elif((11.0*len(mnemonic.split())-check_sum[strength])/strength != 1):
        return '''Provided MNEMONIC in .env file does not match specified strength. Check word count or strength(128 or 256).'''        
    else:
        return mnemonic


################################################################################
# Wallet functionality

###  N.B.> generate account, generate i^th index account, generate 0 thru i accounts.

def generate_account(strength=256,
                     language='english',
                     coin='eth',
                     account_num = 0,
                     change = 0,
                     address_index = 0,
                    ):
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    # Fetch mnemonic from environment variable.
    mnemonic = mnemonic_generator()

    # Create Wallet Object
    wallet = Wallet(mnemonic)

    # Derive Ethereum Private Key
    private, public = wallet.derive_account(coin,
                                           account_num,
                                           change,
                                           address_index)

    # Convert private key into an Ethereum account
    account = Account.privateKeyToAccount(private)

    return account

def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


def send_transaction(w3, account, to, wage):
    """Send an authorized transaction to the Ganache blockchain."""
    # Set gas price strategy
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    # Convert eth amount to Wei
    value = w3.toWei(wage, "ether")

    # Calculate gas estimate
    gasEstimate = w3.eth.estimateGas({"to": to, "from": account.address, "value": value})

    # Construct a raw transaction
    raw_tx = {
        "to": to,
        "from": account.address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": 0,
        "nonce": w3.eth.getTransactionCount(account.address)
    }

    # Sign the raw transaction with ethereum account
    signed_tx = account.signTransaction(raw_tx)

    # Send the signed transactions
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    
    
    
################################################################################
# Bot functionality

###  Bot to connect to RPC server, initialize wallets for admin, clients, and bot;
###  open path to abi, and call SabotStakingV1.sol swap function.


def gen_wallets(num=4,
                bot_wallet=4):
    
    wallet_addresses={}
    for i in range(num):
        key='wallet_'+str(i+1)
        if i ==bot_wallet-1:
            key='bot_wallet'
        wallet_addresses[key]={'account':generate_account(address_index=i)}
        wallet_addresses[key]['address']=wallet_addresses[key]['account'].address
    return wallet_addresses
    

def add_info_to_env(key,info, env_path='./.env'):
    with open(env_path,'a') as f:
        f.write(f"{key}='{info}'\n")    

def open_abi_from_env(env_path='./.env'):    
    try:
        abi_path = os.getenv("SABOTSTAKING_ABI")        
        with open(abi_path,'r') as abi_file:
            abi = json.load(abi_file)
        return abi
    except:
        return '''Path to ABI not found or valid in .env file.'''

def open_contract_address(name):
    try:
        contract_address = os.getenv(name)        
        return contract_address
    except:
        return '''No contract address found in .env file.'''    


def sabot_swap(account, env_path='./.env'):
    assert account is not None, "Account not available."
    assert "USDT_ADDRESS" in os.environ , "USDT_ADDRESS is missing."
    assert "SUSD_ADDRESS" in os.environ , "SUSD_ADDRESS is missing."

    # Connect to .env server
    w3 = connect_RPC_server()
    print(f'Account has balance of:\t{w3.eth.get_balance(account.address)} WEI')
    # Create/read pnemonic in .env file
    #nemo = mnemonic_generator()
    
    # Create wallets
#    wallets=gen_wallets()
    
    # Add info to .env
    # with open(env_path,'a') as f:
    #     f.write('\n')
    # for wallet,info in wallets.items():
    #     key=wallet.upper()
    #     add_info_to_env(key,info['address'])    
    
    # Read path to SabotSwap abi
    sabot_swap_abi = open_abi_from_env()
    
    # Read in sabot contract address
    sabot_contract_address = open_contract_address('SABOT_SWAP_ADDRESS')
    
    # # Generate Contract
    contract = w3.eth.contract(address = sabot_contract_address, abi = sabot_swap_abi)
    print(contract.address)
    print(f'Sabot Contract Address: {sabot_contract_address}')

    # # Create transaction
    base_token = os.environ["USDT_ADDRESS"]
    baseTokenAmount = 10000000
    target_token = os.environ["SUSD_ADDRESS"]
    gas = 3000000
    exchangeRate = 10**18
    
    tx_hash = contract.functions.swap(base_token, baseTokenAmount, target_token, exchangeRate).transact({'from': account.address , 'gas': gas})
    print(contract.functions.name().call())
    receipt = w3.eth.getTransactionReceipt(tx_hash)
    logs = contract.events.Swapped().processReceipt(receipt)
    
    print('here')
    print(logs)
    return 
    

def run(account):
    sabot_swap(account)
    

if __name__=='__main__':
    load_dotenv()

    account =  generate_account(strength=256,
                    language='english',
                    coin='eth',
                    account_num = 0,
                    change = 0,
                    address_index = 3,
                )
    print(f'Account = {account.address}')

    if 'SABOTSTAKING_ABI' not in os.environ:
        print(f'SABOTSTAKING_ABI not in .env')
        print(f'Terminating ...')
        sys.exit()

    if 'SABOT_SWAP_ADDRESS' not in os.environ:
        print(f'SABOT_SWAP_ADDRESS not in .env')
        print(f'Terminating ...')
        sys.exit()

    for i in range(100000):
        run(account)
        time.sleep(4)

