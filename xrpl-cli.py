#!/usr/bin/python3 
#
# xrpl-cli - a command line tool for working with the XRPL, can build with cython.
#
# e.g. 
# list information on accounts
# python3 xrpl-cli.py --network 2 --account rsUjg5ekUMpoJG8NgabUz3WCkpgrkmVUZe
# python3 xrpl-cli.py --account rEx2PsuEurkNQwQbiCeoj1rdAjzu1gX3XF  --network 3 -l
# 
# generate and fund a wallet, mint the token "abcdef" and list NFT's
# python3 xrpl-cli.py -g -n 2 -t abcdef -l
#
# AUTHOR: cove.crypto
# LICENSE: MIT! 
import sys
import json
import xrpl
import argparse
import hashlib
import binascii
import ipfsApi
from xrpl.core import addresscodec
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.transactions import AccountDelete
from xrpl.models.transactions import NFTokenMint
from xrpl.models.transactions import Payment
from xrpl.models.requests import AccountNFTs
from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction, safe_sign_transaction
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.account import get_next_valid_seq_number

# module authorship
__author__ = "Cove Crypto"
__copyright__ = "Copyright Cove Crypto"
__license__ = "MIT"
__version__ = "0.02"

# networks
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
		{"websocket":"wss://xls20-sandbox.rippletest.net:51233"},
		{"jsonrpc":"http://xls20-sandbox.rippletest.net:51234"}
	],
	"local":[
		{"websocket":"wss://127.0.0.1:6006"},
		{"jsonrpc":"http://127.0.0.1:5005"}
	]

}

# XRPL object wrapper around xrpl-py functions
class XRPLobject:
	secret = ""
	account = ""
	owner = ""
	server = ""
	wallet = ""
	# object constructor
	def __init__(self):
		#self.secret = blah
		pass
	# connect over JSON-RPC (only for now, wss more secure for internet)
	def connectrpc(self):
		self.client = JsonRpcClient(self.server)
	# generates a wallet seed from a passphrase, e.g. "masterpassphrase"
	def brainwallet(self,seedkey):
		myseed = hashlib.sha512(seedkey.encode("ascii"))
		myrealseed = myseed.hexdigest().upper()
		seed = binascii.a2b_hex(myrealseed[0:32])
		seed1 = xrpl.core.addresscodec.encode_seed(seed, xrpl.constants.CryptoAlgorithm('secp256k1'))
		self.wallet = xrpl.wallet.Wallet(seed1, 1)
		self.account = self.wallet.classic_address
		self.secret = self.wallet.seed
	# set a wallet seed from cli argument (need to hide this from ps and histfile)
	def seedwallet(self,secret):
		self.wallet = xrpl.wallet.Wallet(secret,1)
		self.account = self.wallet.classic_address
		self.secret = secret
	# use facuet to generate and fund a wallet
	def genwallet(self):
		self.wallet = xrpl.wallet.generate_faucet_wallet(self.client, debug=True)
		self.secret = self.wallet.seed
		self.account = self.wallet.classic_address
	# get the account information
	def getaccount(self):
		acct_info = AccountInfo(account=self.account,ledger_index="validated",strict=True)
		response = self.client.request(acct_info)
		result = response.result
		print("response.status: ", response.status)
		print(json.dumps(response.result, indent=4, sort_keys=True))
	# delete the account
	def delaccount(self,dest):
		current_validated_ledger = get_latest_validated_ledger_sequence(self.client)
		self.wallet.sequence = get_next_valid_seq_number(self.wallet.classic_address, self.client)
		account_delete = AccountDelete(account=self.wallet.classic_address, destination=dest)
		print(account_delete) # the unsigned transaction
		print(account_delete.is_valid())
		account_delete_signed = safe_sign_and_autofill_transaction(account_delete, self.wallet, self.client)
		print(account_delete_signed) # the signed transaction
		tx_response = send_reliable_submission(account_delete_signed, self.client)
		print("response.status: ", tx_response.status)
		print(json.dumps(tx_response.result, indent=4, sort_keys=True))
	def payment(self,dest,amount,tag):
		current_validated_ledger = get_latest_validated_ledger_sequence(self.client)
		self.wallet.sequence = get_next_valid_seq_number(self.wallet.classic_address, self.client)
		if tag == None:
			payment = Payment(account=self.wallet.classic_address, amount=amount, destination=dest)
		else:
			payment = Payment(account=self.wallet.classic_address, amount=amount, destination=dest, destination_tag = tag)
		print(payment) # the unsigned transaction
		print(payment.is_valid())
		payment_signed = safe_sign_and_autofill_transaction(payment, self.wallet, self.client)
		print(payment_signed) # the signed transaction
		tx_response = send_reliable_submission(payment_signed, self.client)
		print("response status: ", tx_response.status)
		print(json.dumps(tx_response.result, indent=4, sort_keys=True))
	# should take taxon as an argument for collections, grouped by taxon as an ID. 
	def mintnft(self,metauri):
		# get the current block height 
		current_validated_ledger = get_latest_validated_ledger_sequence(self.client)
		self.wallet.sequence = get_next_valid_seq_number(self.wallet.classic_address, self.client)
		uriarg = metauri.encode('utf-8')
		uriarg_hex = uriarg.hex()
		# set to 0 by default for taxon, should contain collection ID.
		nft_mint = NFTokenMint(account=self.wallet.classic_address, nftoken_taxon=0, uri=uriarg_hex)
		print(nft_mint) # the unsigned transaction
		print(nft_mint.is_valid())
		nft_mint_signed = safe_sign_and_autofill_transaction(nft_mint, self.wallet, self.client)
		print(nft_mint_signed) # the signed transaction
		tx_response = send_reliable_submission(nft_mint_signed, self.client)
		print("response.status: ", tx_response.status)
		print(json.dumps(tx_response.result, indent=4, sort_keys=True))
	# list NFT tokens and information on account, don't parse any metadata here. 
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
	def get_offers():
		pass
	def accept_sell():
		pass
	def accept_buy():
		pass
	def cancel_offer():
		pass

# main function, entrypoint
if __name__ == "__main__":
	# cli parser and option handling
	parser = argparse.ArgumentParser(description="A command-line interface for working with the XRPL")
	parser.add_argument("-b","--brainwallet", help="use a brain wallet passphrase")
	parser.add_argument("-a","--account", help="classic account address")
	parser.add_argument("-s","--secret", help="seed key")
	parser.add_argument("-pay","--payment", help="send payment of amount")
	parser.add_argument("-tag","--tag", help="optional tag for payment")
	parser.add_argument("-d","--destination", help="destination wallet for transaction")
	parser.add_argument("-g","--generate_wallet", help="generate a wallet from faucet", nargs='?', const=1)
	parser.add_argument("-rm","--delete", help="delete wallet and send balance to destination", nargs='?')
	parser.add_argument("-l","--listnft", help="list nft's on account", nargs='?', const=1)
	parser.add_argument("-t","--tokenurl", help="mint a NFT token url")
	parser.add_argument("-f","--flags", help="NFT flags")
	parser.add_argument("-i","--tokenid", help="token id")
	parser.add_argument("-m","--amount", help="amount")
	parser.add_argument("-x","--tokenofferindex", help="tokenofferindex")
	parser.add_argument("-o","--owner", help="owner")
	parser.add_argument("-n","--network", help="use with list for server list")
	args = parser.parse_args()
	# create the XRPL object
	xrplobj = XRPLobject()
	# configure network node for interaction with XRPL
	if str(args.network) == "list":
		print("0 = main, 1 = testnet, 2 = devnet, 3 = nftdev, 4 = local")
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
		if networkint == 4:
			XRPLobject.server = str(networks["local"][1]["jsonrpc"])
	else:
		print("fatal error, no network selected")
		sys.exit(0)
	# connect to XPRL
	xrplobj.connectrpc()
	# set an account
	if args.account:
		xrplobj.account = args.account
	# make a brain wallet
	if args.brainwallet:
		xrplobj.brainwallet(args.brainwallet)
	# use a wallet secret (need to overwrite argv handler to scrub seed from memory via Cython) 
	if args.secret:
		xrplobj.secret = args.secret
		xrplobj.seedwallet(xrplobj.secret)
	# generate wallet from faucet
	if args.generate_wallet:
		xrplobj.genwallet()
		print("Your secret seed is: %s" % xrplobj.secret)
	if args.delete:
		xrplobj.delwallet(args.delete)
	# mint a URI
	if args.tokenurl:
		if xrplobj.account:
			xrplobj.mintnft(args.tokenurl)
	# list a URI
	if args.listnft:
		if xrplobj.account:
			xrplobj.getnft()
	# send xrp droplets
	if args.payment:
		if args.destination and args.tag:
			xrplobj.payment(args.destination,args.payment,int(args.tag))
		elif args.destination and not args.tag:
			xrplobj.payment(args.destination,args.payment,None)
		else:
			print("Not enough parameters for payment, check your command")
	# default get account details
	if xrplobj.account:
		xrplobj.getaccount()
		sys.exit(0)
