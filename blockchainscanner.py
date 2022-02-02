import json
import appdata
import math
from web3 import Web3
import etherscan
import getdata
import eth_abi
import eth_utils

web3 = Web3(Web3.HTTPProvider(appdata.infura_url))

# scanning throughout the blocks to find operation with the contract
for block_number in range(13679300, 13679301):
    if block_number % 1 == 0:
        print("Scanning block #" + str(block_number))
    block = web3.eth.get_block(block_number)
    transactions_in_block = block['transactions']
    for transaction_hex in transactions_in_block:
        transaction_info = web3.eth.get_transaction(transaction_hex)
        transaction_contract = transaction_info['to']
        if transaction_contract == appdata.address_hoge:
            transaction_bytecode = transaction_info['input']
            print(transaction_bytecode)
            print("\nFind contract transaction in block " + str(block_number))
            print(transaction_info)