from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))
import time
# import json
# from pathlib import Path
# from crypto_wallet import generate_account, get_balance,send_transaction

def handle_event(event):
    print(event)

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

def main():
    # block_filter = w3.eth.filter('latest')
    event_filter = w3.eth.filter({"address": contract_address})
    log_loop(block_filter, 2)

if __name__ == '__main__':
    main()