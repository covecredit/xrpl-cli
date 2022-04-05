#!/usr/bin/env python3
# xrpl-cli - a command line tool for working with the XRPL ledger
# e.g. python3 xrpl-cli.py --account rsUjg5ekUMpoJG8NgabUz3WCkpgrkmVUZe
import sys
import json
import argparse
from xrpl.core import addresscodec
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo

JSON_RPC_URL = "http://xls20-sandbox.rippletest.net:51234"

networks = {
	"main":[
		{"websocket":"https://s1.ripple.com:51234/"},
		{"jsonrpc":"wss://s1.ripple.com/"}
	]
	"testnet":[
		{"websocket":"wss://s.altnet.rippletest.net:51233"},
		{"jsonrpc:""https://s.altnet.rippletest.net:51234"}
	]
	"devnet":[
		{"websocket":"wss://s.devnet.rippletest.net:51233"},
		{"jsonrpc":"https://s.devnet.rippletest.net:51234"}
	]
	"nftdev":[
		{"nftdev":"wss://xls20-sandbox.rippletest.net:51233"},
		{"jsonrpc":"http://xls20-sandbox.rippletest.net:51234"}
	]
}

#genfund
#mint
#get
#burn
#create_sell
#create_buy
#get_offers
#accept_sell
#accept_buy
#cancel_offer

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="A command-line interface for working with the XRPL ledger")
	parser.add_argument("-a","--account", help="classic account address")
	parser.add_argument("-s","--secret", help="seed key")
	parser.add_argument("-t","--tokenurl", help="NFT token url")
	parser.add_argument("-f","--flags", help="NFT flags")
	parser.add_argument("-i","--tokenid", help="token id")
	parser.add_argument("-m","--amount", help="amount")
	parser.add_argument("-x","--tokenofferindex", help="tokenofferindex")
	parser.add_argument("-o","--owner", help="owner")
	args = parser.parse_args()

# query the account arg.
	client = JsonRpcClient(JSON_RPC_URL)
	acct_info = AccountInfo(account=args.account,ledger_index="validated",strict=True)
	response = client.request(acct_info)
	result = response.result
	print("response.status: ", response.status)
	print(json.dumps(response.result, indent=4, sort_keys=True))
