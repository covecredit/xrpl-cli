#!/usr/bin/env python3
# generate an XLS-20 wallet, fund it, mint a file onto the sandbox, host the file on a local IPFS node.
# e.g. python mint.py <filename>
# will put the file onto IPFS and mint it as an NFT
import json
import sys
import os
import argparse
import binascii
import ipfsApi
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.core import addresscodec
from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction, safe_sign_transaction
from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.transactions import NFTokenMint
from xrpl.models.requests import AccountNFTs
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.account import get_next_valid_seq_number

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Supply a filename to mint and store on IPFS")
        sys.exit(0)
    JSON_RPC_URL = "https://s.altnet.rippletest.net:51234"
    client = JsonRpcClient(JSON_RPC_URL)
    test_wallet = generate_faucet_wallet(
        client, debug=True)
    print(test_wallet)
    print(test_wallet.seed)
    acct_info = AccountInfo(
        account=test_wallet.classic_address, ledger_index="validated", strict=True)
    print(acct_info)
    response = client.request(acct_info)
    result = response.result
    print("response.status: ", response.status)
    print(json.dumps(response.result, indent=4, sort_keys=True))
    # list nfts
    nft_info = AccountNFTs(account=test_wallet.classic_address)
    print(nft_info)
    response = client.request(nft_info)
    result = response.result
    print("response.status: ", response.status)
    print(json.dumps(response.result, indent=4, sort_keys=True))
    # connect to IPFS and push the file.
    ipfsclient = ipfsApi.Client()
    os.stat(sys.argv[1])
    ipfsresult = ipfsclient.add(sys.argv[1])
    ipfshash = "ipfs://" + ipfsresult['Hash']
    print("your ipfs file is available at " + ipfshash)
    # get the current block height
    current_validated_ledger = get_latest_validated_ledger_sequence(client)
    test_wallet.sequence = get_next_valid_seq_number(
        test_wallet.classic_address, client)
    # nft_mint uri must be > 5 chars < 512 chars
    # nftoken_taxon = Required, but if you have no use for it, set to zero.
    # uri needs to be hex-encoded data for the transaction
    uriarg = ipfshash.encode('utf-8')
    uriarg_hex = uriarg.hex()
    nft_mint = NFTokenMint(
        account=test_wallet.classic_address, nftoken_taxon=0, uri=uriarg_hex)
    print(nft_mint)  # the unsigned transaction
    print(nft_mint.is_valid())
    nft_mint_signed = safe_sign_and_autofill_transaction(
        nft_mint, test_wallet, client)
    print(nft_mint_signed)  # the signed transaction
    tx_response = send_reliable_submission(nft_mint_signed, client)
    print("response.status: ", tx_response.status)
    print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    # list nfts
    nft_info = AccountNFTs(account=test_wallet.classic_address)
    response = client.request(nft_info)
    result = response.result
    print("response.status: ", response.status)
    print(json.dumps(response.result, indent=4, sort_keys=True))
