#!/usr/bin/env python3
#  
# walks the main net, extracts each transaction, checks for NFT's, finds the metadata, outputs 
#
import json
import sys
import argparse
import binascii
from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet
from xrpl.core import addresscodec
from xrpl.transaction import send_reliable_submission, safe_sign_and_autofill_transaction, safe_sign_transaction
from xrpl.models.requests.account_info import AccountInfo
from xrpl.models.transactions import NFTokenMint
from xrpl.models.requests import AccountNFTs
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.models.requests import Ledger, Tx
from xrpl.account import get_next_valid_seq_number


if __name__ == "__main__":
    JSON_RPC_URL = "https://s1.ripple.com:51234/"
    client = JsonRpcClient(JSON_RPC_URL)
    print("Watching for NFT's...")
    while True:
        ledger_request = Ledger(ledger_index="validated", transactions=True)
        ledger_response = client.request(ledger_request)
        #print(ledger_response)
        transactions = ledger_response.result["ledger"]["transactions"]
        # walk all the transactions in the block
        if len(transactions)==0:
            print("no transactions in this block, are you on dev?")
        for index in range(0,len(transactions)-1):
            tx_request = Tx(transaction=transactions[index])
            tx_response = client.request(tx_request)
            result = tx_response.result
            #print(tx_response.result['TransactionType'])
            if tx_response.result['TransactionType'] == "NFTokenMint":
                # the transaction is a new NFT token mint!
                #print("response.status: ", tx_response.status)
                #print(tx_response.result['TransactionType'])
                metadata = tx_response.result['meta']   
                try:
                    # somebody minted a new...
                    tokens = metadata['AffectedNodes'][0]["CreatedNode"]["NewFields"]["NFTokens"]
                    for nftindex in range(0,len(tokens)-1):
                        nfturihex = tokens[nftindex]["NFToken"]["URI"]
                        nfturibin = binascii.unhexlify(nfturihex)
                        print(nfturibin.decode('UTF-8'))
                except:
                    a = 0
                    #print("not a new mint")
                try:
                    # extract the updated nft uri's, probably an exchange
                    tokens = metadata['AffectedNodes'][0]["ModifiedNode"]["FinalFields"]["NFTokens"]
                    for nftindex in range(0,len(tokens)-1):
                        nfturihex = tokens[nftindex]["NFToken"]["URI"]
                        nfturibin = binascii.unhexlify(nfturihex)
                        print(nfturibin.decode('UTF-8'))
                except:
                    a = 0
                    #print("not an update")
