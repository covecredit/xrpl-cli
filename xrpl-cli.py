#!/usr/bin/env python3
# xrpl-cli - a command line tool for working with the XRPL ledger
# e.g. python3 xrpl-cli.py --account rsUjg5ekUMpoJG8NgabUz3WCkpgrkmVUZe
import sys
import json
import argparse
import hashlib
import binascii
from xrpl.core import addresscodec
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo

networks = {
	"main":[
		{"websocket":"https://s1.ripple.com:51234/"},
		{"jsonrpc":"wss://s1.ripple.com/"}
	],
	"testnet":[
		{"websocket":"wss://s.altnet.rippletest.net:51233"},
		{"jsonrpc:""https://s.altnet.rippletest.net:51234"}
	],
	"devnet":[
		{"websocket":"wss://s.devnet.rippletest.net:51233"},
		{"jsonrpc":"https://s.devnet.rippletest.net:51234"}
	],
	"nftdev":[
		{"nftdev":"wss://xls20-sandbox.rippletest.net:51233"},
		{"jsonrpc":"http://xls20-sandbox.rippletest.net:51234"}
	]
}

class XRPLobject:
	secret = ""
	account = ""
	owner = ""
	server = ""
	def __init__(self):
        	#self.secret = blah
		pass
	def connectrpc():
		self.client = JsonRpcClient(networks["nftdev"][1]["jsonrpc"])
		pass
	def brainwallet(seedkey):
		myseed = hashlib.sha512(seedkey.encode("ascii"))
		myrealseed = myseed.hexdigest().upper()
		seed = binascii.a2b_hex(myrealseed[0:32])
		seed1 = xrpl.core.addresscodec.encode_seed(seed, xrpl.constants.CryptoAlgorithm('secp256k1'))
    		# create a wallet from the seed
		self.wallet = xrpl.wallet.Wallet(seed1, 1)
		pass
	def getaccount():
		acct_info = AccountInfo(account=args.account,ledger_index="validated",strict=True)
		response = self.client.request(acct_info)
		result = response.result
		print("response.status: ", response.status)
		print(json.dumps(response.result, indent=4, sort_keys=True))
		pass
	def fundaccount():
		pass
	def genfund():
		pass
	def mint():
		pass
	def getnft():
		pass
	def burnnft():
		pass
	def create_sell():
		pass
	def create_buy():
		pass
	def create_buy():
		pass
	def get_offers():
		pass
	def accept_sell():
		pass
	def accept_buy():
		pass
	def cancel_offer():
		pass

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

