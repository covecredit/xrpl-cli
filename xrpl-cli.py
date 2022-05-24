#!/usr/bin/env python3
# xrpl-cli - a command line tool for working with the XRPL ledger
# e.g. 
# python3 xrpl-cli.py --network 2 --account rsUjg5ekUMpoJG8NgabUz3WCkpgrkmVUZe
# python3 xrpl-cli.py --account rEx2PsuEurkNQwQbiCeoj1rdAjzu1gX3XF  --network 3 -l
import sys
import json
import xrpl
import argparse
import hashlib
import binascii
from xrpl.core import addresscodec
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.transactions import NFTokenMint
from xrpl.models.requests import AccountNFTs

networks = {
	"main":[
		{"websocket":"wss://s1.ripple.com/"},
		{"jsonrpc":"https://s1.ripple.com:51234/"}
	],
	"testnet":[
		{"websocket":"wss://s.altnet.rippletest.net:51233"},
		{"jsonrpc":"https://s.altnet.rippletest.net:51234"}
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
	def connectrpc(self):
		self.client = JsonRpcClient(self.server)
	def brainwallet(self,seedkey):
		myseed = hashlib.sha512(seedkey.encode("ascii"))
		myrealseed = myseed.hexdigest().upper()
		seed = binascii.a2b_hex(myrealseed[0:32])
		seed1 = xrpl.core.addresscodec.encode_seed(seed, xrpl.constants.CryptoAlgorithm('secp256k1'))
		self.wallet = xrpl.wallet.Wallet(seed1, 1)
		self.account = self.wallet.classic_address
		self.secret = self.wallet.seed
	def seedwallet(self,secret):
		self.wallet = xrpl.wallet.Wallet(secret,1)
		self.account = self.wallet.classic_address
		self.secret = secret
	def genwallet(self):
		self.wallet = xrpl.wallet.generate_faucet_wallet(self.client, debug=True)
		self.secret = self.wallet.seed
		self.account = self.wallet.classic_address
	def getaccount(self):
		acct_info = AccountInfo(account=self.account,ledger_index="validated",strict=True)
		response = self.client.request(acct_info)
		result = response.result
		print("response.status: ", response.status)
		print(json.dumps(response.result, indent=4, sort_keys=True))
	def mintnft(self,metauri):
		nft_mint = NFTokenMint(account=self.account, token_taxon=0, uri=metauri)
		print(nft_mint)
		print(nft_mint.is_valid())
		response = self.client.request(nft_mint)
		result = response.result
		print("response.status: ", response.status)
		print(json.dumps(response.result, indent=4, sort_keys=True))
	def getnft(self):
		nft_info = AccountNFTs(account=self.account)
		response = self.client.request(nft_info)
		result = response.result
		print("response.status: ", response.status)
		print(json.dumps(response.result, indent=4, sort_keys=True))
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
	parser.add_argument("-b","--brainwallet", help="use a brain wallet passphrase")
	parser.add_argument("-a","--account", help="classic account address")
	parser.add_argument("-s","--secret", help="seed key")
	parser.add_argument("-g","--generate_wallet", help="generate a wallet from faucet", nargs='?', const=1)
	parser.add_argument("-l","--listnft", help="list nft's on account", nargs='?', const=1)
	parser.add_argument("-t","--tokenurl", help="mint a NFT token url")
	parser.add_argument("-f","--flags", help="NFT flags")
	parser.add_argument("-i","--tokenid", help="token id")
	parser.add_argument("-m","--amount", help="amount")
	parser.add_argument("-x","--tokenofferindex", help="tokenofferindex")
	parser.add_argument("-o","--owner", help="owner")
	parser.add_argument("-n","--network", help="use with list for server list")
	args = parser.parse_args()
	xrplobj = XRPLobject()
	if str(args.network) == "list":
		print("0 = main, 1 = testnet, 2 = devnet, 3 = nftdev")
		print(networks)
		sys.exit(0)
	try:
		networkint = int(args.network)
	except:
		print("select a network, use --help")
		sys.exit(0)
	if int(networkint) > -1:
		if networkint == 0:
			XRPLobject.server = str(networks["main"][1]["jsonrpc"])
		if networkint == 1:
			XRPLobject.server = str(networks["testnet"][1]["jsonrpc"])
		if networkint == 2:
			XRPLobject.server = str(networks["devnet"][1]["jsonrpc"])
		if networkint == 3:
			XRPLobject.server = str(networks["nftdev"][1]["jsonrpc"])
	else:
		print("fatal error, no network selected")
		sys.exit(0)
	xrplobj.connectrpc()
	# set an account
	if args.account:
                xrplobj.account = args.account
	# make a brain wallet
	if args.brainwallet:
		xrplobj.brainwallet(args.brainwallet)
	# use a wallet secret
	if args.secret:
		xrplobj.secret = args.secret
		xrplobj.seedwallet(xrplobj.secret)
	# generate wallet from faucet
	if args.generate_wallet:
		xrplobj.genwallet()
		print("Your secret seed is: %s" % xrplobj.secret)
	if args.listnft:
		if xrplobj.account:
			xrplobj.getnft()
	# default get account 
	if args.tokenurl:
		xrplobj.mintnft(args.tokenurl)
	if xrplobj.account:
		xrplobj.getaccount()
		sys.exit(0)
