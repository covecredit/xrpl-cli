#!/usr/bin/env python3
# Generate a wallet through a faucet
import json
import sys
import argparse
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.core import addresscodec
from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.transactions import NFTokenMint
from xrpl.models.requests import AccountNFTs

if __name__ == "__main__":
    JSON_RPC_URL = "http://xls20-sandbox.rippletest.net:51234"
    client = JsonRpcClient(JSON_RPC_URL)
    test_wallet = generate_faucet_wallet(
        client, debug=True, faucet_host="faucet-nft.ripple.com")
    print(test_wallet)
    print(test_wallet.seed)
    acct_info = AccountInfo(
        account=test_wallet.classic_address, ledger_index="validated", strict=True)
    response = client.request(acct_info)
    result = response.result
    print("response.status: ", response.status)
    print(json.dumps(response.result, indent=4, sort_keys=True))
    # list nfts
    nft_info = AccountNFTs(account=test_wallet.classic_address)
    response = client.request(nft_info)
    result = response.result
    print("response.status: ", response.status)
    print(json.dumps(response.result, indent=4, sort_keys=True))

    # nft_mint
    nft_mint = NFTokenMint(account=test_wallet.classic_address, token_taxon=0, uri="\x41\x42\x43\x44")
    print(nft_mint)
    print(nft_mint.is_valid())
    response = client.request(nft_mint)
    result = response.result
    print("response.status: ", response.status)
    print(json.dumps(response.result, indent=4, sort_keys=True))
