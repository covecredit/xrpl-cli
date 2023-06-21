#!/usr/bin/env python3
# XRPL ripple "brain wallet" generate
# ===================================
# Generates a "brain wallet" seed as per the rippled
# implementation of sha512 halving to produce a 128-bit
# key when the entropy input for the key is a mnemonic.
import json
import sys
import xrpl
import hashlib
import binascii
from xrpl.clients import JsonRpcClient
from xrpl.core import addresscodec
from xrpl.models.requests.account_info import AccountInfo

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Supply a <passphrase> to test")
        sys.exit()
    # generate a wallet from a brain passphrase
    seedkey = sys.argv[1]
    myseed = hashlib.sha512(seedkey.encode("ascii"))
    myrealseed = myseed.hexdigest().upper()
    seed = binascii.a2b_hex(myrealseed[0:32])
    print("Generating brain wallet with phrase: " + seedkey)
    print(seed)
    seed1 = xrpl.core.addresscodec.encode_seed(
        seed, xrpl.constants.CryptoAlgorithm('secp256k1'))
    # create a wallet form the seed
    test_wallet = xrpl.wallet.Wallet(seed1, 1)
    print(test_wallet)
    print(test_wallet.seed)
