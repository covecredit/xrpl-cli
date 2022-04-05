#!/usr/bin/env python3
import sys
import json
import argparse
from xrpl.core import addresscodec
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.models.requests.account_info import AccountInfo

JSON_RPC_URL = "http://xls20-sandbox.rippletest.net:51234"

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

#--account
#--secret
#--tokenurl
#--flags
#--tokenid
#--amount
#--tokenofferindex
#--owner

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("account")
	args = parser.parse_args()
	client = JsonRpcClient(JSON_RPC_URL)
	acct_info = AccountInfo(account=args.account,ledger_index="validated",strict=True)
	response = client.request(acct_info)
	result = response.result
	print("response.status: ", response.status)
	print(json.dumps(response.result, indent=4, sort_keys=True))
