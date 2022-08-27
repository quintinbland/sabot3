from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
import time
import json
from pathlib import Path
from datetime import datetime
import csv
from dotenv import load_dotenv
load_dotenv()
import os

writer = None

def handle_event(contract,event_raw):
    global writer
    receipt = w3.eth.getTransactionReceipt(event_raw['transactionHash'])
    print (receipt)
    swapped_event = contract.events.Swapped().processReceipt(receipt)
    print(f"swapped_event: {swapped_event}")
    minted_event = contract.events.Minted().processReceipt(receipt)
    print(f"minted_event: {minted_event}")
    staked_event = contract.events.Staked().processReceipt(receipt)  
    print(f"staked_event: {staked_event}")
    event_record = {
        'time':datetime.now().timestamp(),
        'type':None,
        'sellToken':None,
        'sellTokenAmount':None,
        'buyToken':None,
        'buyTokenAmount':None,
        'utilityToken':None,
        'utilityTokenAmount':None,
        'owner':None
    }
    if swapped_event is not None and len(swapped_event)>0 and 'event' in swapped_event[0]:
        event_record['type']='Swapped'
        if 'args' in swapped_event[0]:
            for key,value in swapped_event[0]['args'].items():
                event_record[key]=value
    if minted_event is not None and len(minted_event)>0 and 'event' in minted_event[0]:
        event_record['type']='Minted'
        if 'args' in minted_event[0]:
            for key,value in minted_event[0]['args'].items():
                event_record[key]=value
    if staked_event is not None and len(staked_event)>0 and 'event' in staked_event[0]:
        event_record['type']='Staked'
        if 'args' in staked_event[0]:
            for key,value in staked_event[0]['args'].items():
                event_record[key]=value
    print(event_record)
    if writer is not None:
        writer.writerow(event_record)     
        # writer.

def log_loop(contract,contract_filter, poll_interval):
    while True:
        logs = w3.eth.getFilterChanges(contract_filter.filter_id)
        for event in logs:
            handle_event(contract,event)
        # for event in event_filter.get_new_entries():
        #     handle_event(event)
        time.sleep(poll_interval)

def main():
    global writer
    event_record = {
        'time':datetime.now().timestamp(),
        'type':None,
        'sellToken':None,
        'sellTokenAmount':None,
        'buyToken':None,
        'buyTokenAmount':None,
        'utilityToken':None,
        'utilityTokenAmount':None,
        'owner':None
    }

    event_log_path = Path(os.environ['EVENT_LOG'])
    if not event_log_path.exists():
        with open(event_log_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=event_record.keys())
            writer.writeheader()    
    # block_filter = w3.eth.filter('latest')
    abi=None
    with open(Path('data/SabotSwapBase_abi.json'),'r') as abi_file:
        abi = json.load(abi_file)    
    contract_address = '0x3a83052fd36aFb70adC754eD380EE3EBCD295400'
   
    contract = w3.eth.contract(address = contract_address , abi = abi)    
    contract_filter = w3.eth.filter({"address": contract_address})
    with open(event_log_path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=event_record.keys())
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
