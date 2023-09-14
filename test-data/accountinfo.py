#!/usr/bin/env python3
# AccountInfo 
# - looks up public wallet address and returns account data
import json
import sys
import xrpl
import hashlib
from xrpl.clients import JsonRpcClient
from xrpl.core import addresscodec
from xrpl.models.requests.account_info import AccountInfo

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Supply a <account> value to verify")
        sys.exit()
    JSON_RPC_URL = "https://s1.ripple.com:51234/"
    client = JsonRpcClient(JSON_RPC_URL)
    acct_info = AccountInfo(
        account=sys.argv[1], ledger_index="validated", strict=True)
    response = client.request(acct_info)
    print(json.dumps(response.result, indent=4, sort_keys=True))
    lsfDisableMaster = 0x00100000
    acct_flags = response.result["account_data"]["Flags"]
    if lsfDisableMaster & acct_flags == lsfDisableMaster:
        print("Master key pair is DISABLED")
    else:
        print("Master key pair is available for use")
