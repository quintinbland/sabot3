from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
import time
import json
from pathlib import Path
# from crypto_wallet import generate_account, get_balance,send_transaction

def handle_event(contract,event_raw):
    # SabotSwap event defines args sellToken, sellTokenAmount, buyToken, buyTokenAmount
    receipt = w3.eth.getTransactionReceipt(event_raw['transactionHash'])
    # SabotSwap event defines args sellToken, sellTokenAmount, buyToken, buyTokenAmount
    swap_event = contract.events.SabotSwap().processReceipt(receipt)[0]  
    # Minted eventSabotSwap event defines clogAmount, owner
    minted_event = contract.events.Minted().processReceipt(receipt)[0]  
    # Staking event defines args owner, sellToken, sellTokenAmount, clogAmount
    staking_event = contract.events.Staking().processReceipt(receipt)[0]  
    if swap_event is not None and 'event' in swap_event:
        args = f"event: {swap_event['event']}\n"
        if 'args' in swap_event:
            for key,value in swap_event['args'].items():
                args += f"\t{key}={value}\n"
        print(args)
    if minting_event is not None and 'event' in minting_event:
        args = f"event: {minting_event['event']}\n"
        if 'args' in minting_event:
            for key,value in minting_event['args'].items():
                args += f"\t{key}={value}\n"
        print(args)
    if staking_event is not None and 'event' in staking_event:
        args = f"event: {staking_event['event']}\n"
        if 'args' in staking_event:
            for key,value in staking_event['args'].items():
                args += f"\t{key}={value}\n"
        print(args)

def log_loop(contract,contract_filter, poll_interval):
    while True:
        logs = w3.eth.getFilterChanges(contract_filter.filter_id)
        for event in logs:
            handle_event(contract,event)
        # for event in event_filter.get_new_entries():
        #     handle_event(event)
        time.sleep(poll_interval)

def main():
    # block_filter = w3.eth.filter('latest')
    abi=None
    with open(Path('SabotSwapBase_abi.json'),'r') as abi_file:
        abi = json.load(abi_file)    
    contract_address = '0x3830a870dE6b28AF2999A8A6944e9D6042A82861'
   
    contract = w3.eth.contract(address = contract_address , abi = abi)    
    contract_filter = w3.eth.filter({"address": contract_address})
    log_loop(contract,contract_filter, 2)

if __name__ == '__main__':
    main()



# (
#     AttributeDict(
#         {'args': AttributeDict(
#             {'sellToken': '0x04324f495a27fa08d5E8CC3F01178F55C46D53bf', 
#             'sellTokenAmount': 777770000000, 
#             'buyToken': '0x6e8d8c332fAF8b71E312F5377D9dd94baDE0d744', 
#             'buyTokenAmount': 42}), 
#          'event': 'SabotSwap', 
#          'logIndex': 0, 
#          'transactionIndex': 0, 
#          'transactionHash': HexBytes('0xb7dbc427ceffb328067823169b79461ffeffc0811a585e2dfc1ab691d8ef53df'), 
#          'address': '0x3830a870dE6b28AF2999A8A6944e9D6042A82861', 
#          'blockHash': HexBytes('0xa13bdd7e7684152f3ff6b59a6d4a2057b7ccf829029844d46f61273bf4378b15'), 
#          'blockNumber': 39})
# ,)
