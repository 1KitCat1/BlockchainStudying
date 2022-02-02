import json
import appdata
import math
from web3 import Web3
import etherscan
import getdata
import eth_abi
import eth_utils

web3 = Web3(Web3.HTTPProvider(appdata.infura_url))

smart_transaction_info = web3.eth.get_transaction('0x33a00225ba2d73059ade4f737d2dc8f8b565ec914872242fc0189448c5b84e22')
smart_transaction_receipt = web3.eth.get_transaction_receipt('0x33a00225ba2d73059ade4f737d2dc8f8b565ec914872242fc0189448c5b84e22')
print(smart_transaction_info)
print()
for val in smart_transaction_receipt:
    print(str(val) + ' ' + str(smart_transaction_receipt[val]))
    print("--")

# smart_transaction_input = smart_transaction_info['input']
# print()
# print(smart_transaction_input)
# print(eth_utils.decode_hex(smart_transaction_input))
# smart_transaction_bytecode = smart_transaction_info['input']
# smart_transaction_abi = eth_abi.decode_abi(['string'], bytes(smart_transaction_bytecode))
# print(smart_transaction_abi)