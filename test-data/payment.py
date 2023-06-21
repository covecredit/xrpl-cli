#!/usr/bin/env python3
# Generate a wallet through a faucet and then delete it, sends balance to rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh
import json
import time
import sys
import argparse
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.core import addresscodec
from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.transactions import Payment
from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction, safe_sign_transaction
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.account import get_next_valid_seq_number

if __name__ == "__main__":
	JSON_RPC_URL = "http://xls20-sandbox.rippletest.net:51234"
	dest = "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh"
	client = JsonRpcClient(JSON_RPC_URL)
	test_wallet = generate_faucet_wallet(client, debug=True,faucet_host="faucet-nft.ripple.com")
	print(test_wallet)
	print(test_wallet.seed)
	acct_info = AccountInfo(account=test_wallet.classic_address,ledger_index="validated",strict=True)
	response = client.request(acct_info)
	result = response.result
	print("response.status: ", response.status)
	print(json.dumps(response.result, indent=4, sort_keys=True))
	# current block height
	current_validated_ledger = get_latest_validated_ledger_sequence(client)
	test_wallet.sequence = get_next_valid_seq_number(test_wallet.classic_address, client)
	# not partial payment, full payment, auto-fill txn fee, invoice id = 256bit hash, memo = arbitary data
	payment = Payment(account=test_wallet.classic_address, amount="1000", destination=dest, destination_tag=1337)
	print(payment) # the unsigned transaction
	print(payment.is_valid())
	# auto fill transaction
	payment_signed = safe_sign_and_autofill_transaction(payment, test_wallet, client)
	print(payment_signed) # the signed transaction
	tx_response = send_reliable_submission(payment_signed, client)
	print("response.status: ", tx_response.status)
	print(json.dumps(tx_response.result, indent=4, sort_keys=True))
