#!/usr/bin/env python3
# test amm_info RPC request
# - lacks pair discovery process
import json
import time
import sys
import argparse
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.core import addresscodec
from xrpl.models.requests import AMMInfo
from xrpl.models.transactions import Payment
from xrpl.transaction import submit_and_wait
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.account import get_next_valid_seq_number

if __name__ == "__main__":
    JSON_RPC_URL = "https://amm.devnet.rippletest.net:51234"
    dest = "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh"
    client = JsonRpcClient(JSON_RPC_URL)
    # XRP can be string, no need for object.
    # all other assets passed as object with currency + issuer.
    amm_info = AMMInfo(asset={"currency": "XRP"}, asset2={
                       "currency": "TST", "issuer": "rP9jPyP5kyvFRb6ZiRghAGw5u8SGAmU4bd"})
    response = client.request(amm_info)
    result = response.result
    print("response.status: ", response.status)
    print(json.dumps(response.result, indent=4, sort_keys=True))
