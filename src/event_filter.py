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
csv_file = None

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

def handle_event(contract,event_raw):
    global writer
    global csv_file
    receipt = w3.eth.getTransactionReceipt(event_raw['transactionHash'])
    swapped_event = contract.events.Swapped().processReceipt(receipt)
    minted_event = contract.events.Minted().processReceipt(receipt)
    burned_event = contract.events.Burned().processReceipt(receipt)
    staked_event = contract.events.Staked().processReceipt(receipt)  
    unstaked_event = contract.events.Unstaked().processReceipt(receipt)  
    exchange_rate_event = contract.events.ExchangeRate().processReceipt(receipt)  
    # events=[]
    if swapped_event is not None and len(swapped_event)>0 and 'event' in swapped_event[0]:
        if 'args' in swapped_event[0]:
            # events.append(make_event_record('Swapped',swapped_event[0]['args']))
            event_record = make_event_record('Swapped',swapped_event[0]['args'])
            print(event_record)
            if writer is not None:
                writer.writerow(event_record)     
    if minted_event is not None and len(minted_event)>0 and 'event' in minted_event[0]:
        if 'args' in minted_event[0]:
            # events.append(make_event_record('Minted',minted_event[0]['args']))
            event_record = make_event_record('Minted',minted_event[0]['args'])
            print(event_record)
            if writer is not None:
                writer.writerow(event_record)     
    if burned_event is not None and len(burned_event)>0 and 'event' in burned_event[0]:
        if 'args' in burned_event[0]:
            # events.append(make_event_record('Burned',burned_event[0]['args']))
            event_record = make_event_record('Burned',burned_event[0]['args'])
            print(event_record)
            if writer is not None:
                writer.writerow(event_record)     
    if staked_event is not None and len(staked_event)>0 and 'event' in staked_event[0]:
        if 'args' in staked_event[0]:
            # events.append(make_event_record('Staked',staked_event[0]['args']))
            event_record = make_event_record('Staked',staked_event[0]['args'])
            print(event_record)
            if writer is not None:
                writer.writerow(event_record)     
    if unstaked_event is not None and len(unstaked_event)>0 and 'event' in unstaked_event[0]:
        if 'args' in unstaked_event[0]:
            # events.append(make_event_record('Unstaked',unstaked_event[0]['args']))
            event_record = make_event_record('Unstaked',unstaked_event[0]['args'])
            print(event_record)
            if writer is not None:
                writer.writerow(event_record)     
    if exchange_rate_event is not None and len(exchange_rate_event)>0 and 'event' in exchange_rate_event[0]:
        if 'args' in exchange_rate_event[0]:
            # events.append(make_event_record('ExchangeRate',exchange_rate_event[0]['args']))
            event_record = make_event_record('ExchangeRate',exchange_rate_event[0]['args'])
            print(event_record)
            if writer is not None:
                writer.writerow(event_record)    
                csv_file.flush()

    # for event_record in events:
    #     print(event_record)
    #     if writer is not None:
    #         writer.writerow(event_record)     
        

def log_loop(contract,contract_filter, poll_interval):
    while True:
        logs = w3.eth.getFilterChanges(contract_filter.filter_id)
        if len(logs)>0:
            event = logs[0]
            handle_event(contract,event)
        time.sleep(poll_interval)

def main():
    global writer
    global csv_file
    event_record = {
        'time':datetime.now().timestamp(),
        'type':None,
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

    event_log_path = Path(os.environ['EVENT_LOG'])
    if not event_log_path.exists():
        with open(event_log_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=event_record.keys())
            writer.writeheader()    
    # block_filter = w3.eth.filter('latest')
    abi=None
    with open(Path(os.environ['SABOTSTAKING_ABI']),'r') as abi_file:
        abi = json.load(abi_file)    
    contract_address = os.environ['SABOT_SWAP_ADDRESS']
   
    contract = w3.eth.contract(address = contract_address , abi = abi)    
    contract_filter = w3.eth.filter({"address": contract_address})
    with open(event_log_path, 'a') as csvfile:
        csv_file = csvfile
        writer = csv.DictWriter(csvfile, fieldnames=event_record.keys())
        log_loop(contract,contract_filter, 2)

if __name__ == '__main__':
    main()

