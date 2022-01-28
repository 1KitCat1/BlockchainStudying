import json
import appdata
import math
from web3 import Web3
import etherscan
import getdata

# connection
etherscn = etherscan.Client(appdata.etherscan_api)
web3 = Web3(Web3.HTTPProvider(appdata.infura_url))

# connect to contracts
uniswapContract = web3.eth.contract(address=Web3.toChecksumAddress(appdata.address_uniswap), abi=appdata.abi_uniswap)
pairContract = web3.eth.contract(address=appdata.address_hoge, abi=appdata.abi_hoge)

# get liquidity pools
[pooledETH, pooledHOGE, t] = pairContract.functions.getReserves().call()

# try to update latest transaction
last_block = web3.eth.get_block('latest')
last_block_transactions = last_block['transactions']
try:
    appdata.transaction_hash = last_block_transactions[0]
    print("Info about latest transaction updated")
except:
    print("No transaction in latest block. Using default transaction to calculate gas fees")

# get transaction data
transaction_info = web3.eth.getTransaction(appdata.transaction_hash)
transaction_receipt = web3.eth.getTransactionReceipt(appdata.transaction_hash)

# get fee data
transaction_gasPrice = transaction_receipt['effectiveGasPrice']
transaction_gasUsed = transaction_receipt['gasUsed']
transaction_fee_wei = transaction_gasPrice * transaction_gasUsed
transaction_fee_eth = web3.fromWei(transaction_fee_wei, 'ether')
transaction_fee_usd = getdata.get_current_data(from_sym='ETH', to_sym='USD')['USD'] * float(transaction_fee_eth)

# attack info
victim_transaction = 2 # amount of ether victim is going to swap
adversaries_transaction = 2 # amount of ether adversaries is going to swap

# calculation
before_price = pooledETH / pooledHOGE
after_pooledETH = pooledETH + web3.toWei(adversaries_transaction, 'ether')
amount_HOGE_adversarie_get = (web3.toWei(adversaries_transaction, 'ether') / before_price)
after_pooledHOGE = pooledHOGE - amount_HOGE_adversarie_get
after_price = after_pooledETH / after_pooledHOGE
print("Price before frontrunning attack: " + str(before_price))
print("Price after frontrunning attack: " + str(after_price))

afterVic_pooledETH = after_pooledETH + web3.toWei(victim_transaction, 'ether')
amount_HOGE_victim_get = (web3.toWei(victim_transaction, 'ether') / after_price)
afterVic_pooledHOGE = after_pooledHOGE - amount_HOGE_victim_get
afterVic_price = afterVic_pooledETH / afterVic_pooledHOGE
print("Price after victim transaction: " + str(afterVic_price))

amount_eth_advers_after = amount_HOGE_adversarie_get * afterVic_price
count_commission = float(web3.fromWei(amount_eth_advers_after, 'ether')) - 2*(adversaries_transaction * .03 + float(transaction_fee_eth)) - adversaries_transaction
print("Amount of extra eth attacker gets back:  " + str(count_commission))

