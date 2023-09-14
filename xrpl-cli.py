#!/usr/bin/python3
# xrpl-cli - a command line tool for working with the XRPL, can build with cython.
# ================================================================================
#
# e.g.
# list information on accounts
#
# python3 xrpl-cli.py --network 2 --account rsUjg5ekUMpoJG8NgabUz3WCkpgrkmVUZe
# python3 xrpl-cli.py --account rEx2PsuEurkNQwQbiCeoj1rdAjzu1gX3XF --network 3 -l
#
# generate and fund a wallet, mint the token "abcdef" and list NFT's
# python3 xrpl-cli.py -g -n 2 -t abcdef -l
#
# generate a funded wallet, send XRP to the XRP master wallet on test.
# python3 xrpl-cli.py -n 1 -g -p 99999999 -d rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh
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
# import all XRPL transaction models
from xrpl.models.transactions import *
# import AccountNFT request
from xrpl.models.requests import AccountNFTs
from xrpl.transaction import submit_and_wait
from xrpl.ledger import get_latest_validated_ledger_sequence
from xrpl.account import get_next_valid_seq_number

# module authorship
__author__ = "Cove Crypto"
__copyright__ = "Copyright Cove Crypto"
__license__ = "MIT"
__version__ = "0.02"

# networks
networks = {
    "main": [
        {"websocket": "wss://s1.ripple.com/"},
        {"jsonrpc": "https://s1.ripple.com:51234/"}
    ],
    "testnet": [
        {"websocket": "wss://s.altnet.rippletest.net:51233"},
        {"jsonrpc": "https://s.altnet.rippletest.net:51234"}
    ],
    "devnet": [
        {"websocket": "wss://s.devnet.rippletest.net:51233"},
        {"jsonrpc": "https://s.devnet.rippletest.net:51234"}
    ],
    "ammdev": [
        {"websocket": "wss://amm.devnet.rippletest.net:51233"},
        {"jsonrpc": "https://amm.devnet.rippletest.net:51234"}
    ],
    "local": [
        {"websocket": "wss://127.0.0.1:6006"},
        {"jsonrpc": "http://127.0.0.1:5005"}
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
        # self.secret = blah
        pass
    # connect over JSON-RPC (only for now, wss more secure for internet)

    @classmethod
    def connectrpc(self):
        self.client = JsonRpcClient(self.server)
    # generates a wallet seed from a passphrase, e.g. "masterpassphrase"

    @classmethod
    def brainwallet(self, seedkey):
        myseed = hashlib.sha512(seedkey.encode("ascii"))
        myrealseed = myseed.hexdigest().upper()
        seed = binascii.a2b_hex(myrealseed[0:32])
        seed1 = xrpl.core.addresscodec.encode_seed(
            seed, xrpl.constants.CryptoAlgorithm('secp256k1'))
        self.wallet = xrpl.wallet.Wallet.from_secret(seed1)
        self.account = self.wallet.classic_address
        self.secret = self.wallet.seed
    # set a wallet seed from cli argument (need to hide this from ps and histfile)

    @classmethod
    def seedwallet(self, secret):
        self.wallet = xrpl.wallet.Wallet(secret, 1)
        self.account = self.wallet.classic_address
        self.secret = secret
    # use facuet to generate and fund a wallet

    @classmethod
    def genwallet(self):
        self.wallet = xrpl.wallet.generate_faucet_wallet(
            self.client, debug=True)
        self.secret = self.wallet.seed
        self.account = self.wallet.classic_address
    # get the account information

    @classmethod
    def getaccount(self):
        acct_info = AccountInfo(account=self.account,
                                ledger_index="validated", strict=True)
        response = self.client.request(acct_info)
        result = response.result
        print("response.status: ", response.status)
        print(json.dumps(response.result, indent=4, sort_keys=True))
    # delete the account

    @classmethod
    def delaccount(self, dest):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        account_delete = AccountDelete(
            account=self.wallet.classic_address, destination=dest)
        print(account_delete)  # the unsigned transaction
        print(account_delete.is_valid())
        # account_delete_signed = safe_sign_and_autofill_transaction(account_delete, self.wallet, self.client)
        # print(account_delete_signed) # the signed transaction
        tx_response = submit_and_wait(account_delete, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    # sign a payment transaction message and send

    @classmethod
    def payment(self, dest, amount, source_tag=None, destination_tag=None):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        if destination_tag == None:
            payment = Payment(account=self.wallet.classic_address,
                              amount=amount, destination=dest)
        else:
            payment = Payment(account=self.wallet.classic_address,
                              amount=amount, destination=dest, destination_tag=tag)
        print(payment)  # the unsigned transaction
        print(payment.is_valid())
        # payment_signed = safe_sign_and_autofill_transaction(payment, self.wallet, self.client)
        # print(payment_signed) # the signed transaction
        tx_response = submit_and_wait(payment, self.client, self.wallet)
        print("response status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    # should take taxon as an argument for collections, grouped by taxon as an ID.

    @classmethod
    def mintnft(self, metauri):
        # get the current block height
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        uriarg = metauri.encode('utf-8')
        uriarg_hex = uriarg.hex()
        # set to 0 by default for taxon, should contain collection ID.
        nft_mint = NFTokenMint(
            account=self.wallet.classic_address, nftoken_taxon=0, uri=uriarg_hex)
        print(nft_mint)  # the unsigned transaction
        print(nft_mint.is_valid())
        # nft_mint_signed = safe_sign_and_autofill_transaction(nft_mint, self.wallet, self.client)
        # print(nft_mint_signed) # the signed transaction
        tx_response = submit_and_wait(nft_mint, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))
    # list NFT tokens and information on account, don't parse any metadata here.

    @classmethod
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

    @classmethod
    def check_cancel(self, check_id):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        check_cancel = CheckCancel(
            account=self.wallet.classic_address, check_id=check_id)
        print(check_cancel)  # the unsigned transaction
        print(check_cancel.is_valid())
        # check_cancel_signed = safe_sign_and_autofill_transaction(check_cancel, self.wallet, self.client)
        # print(check_cancel_signed)  # the signed transaction
        tx_response = submit_and_wait(check_cancel, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def check_cash(self, check_id, amount):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        check_cash = CheckCash(
            account=self.wallet.classic_address, check_id=check_id, amount=amount)
        print(check_cash)  # the unsigned transaction
        print(check_cash.is_valid())
        # check_cash_signed = safe_sign_and_autofill_transaction(check_cash, self.wallet, self.client)
        # print(check_cash_signed)  # the signed transaction
        tx_response = submit_and_wait(check_cash, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def deposit_preauth(self, authorized_address, destination_address, remove=False):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        deposit_preauth = DepositPreauth(account=self.wallet.classic_address,
                                         authorize=authorized_address, unauthorize=destination_address if remove else None)
        print(deposit_preauth)  # the unsigned transaction
        print(deposit_preauth.is_valid())
        # deposit_preauth_signed = safe_sign_and_autofill_transaction(deposit_preauth, self.wallet, self.client)
        # print(deposit_preauth_signed)  # the signed transaction
        tx_response = submit_and_wait(
            deposit_preauth_signed, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def escrow_cancel(self, owner_address, offer_sequence):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        escrow_cancel = EscrowCancel(
            account=self.wallet.classic_address,
            owner=owner_address,
            offer_sequence=offer_sequence
        )
        print(escrow_cancel)  # the unsigned transaction
        print(escrow_cancel.is_valid())
        # escrow_cancel_signed = safe_sign_and_autofill_transaction(escrow_cancel, self.wallet, self.client)
        # print(escrow_cancel_signed)  # the signed transaction
        tx_response = submit_and_wait(
            escrow_cancel_signed, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def escrow_create(self, amount, destination, cancel_after, finish_after, condition, source_tag=None, destination_tag=None):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        escrow_create = EscrowCreate(
            account=self.wallet.classic_address,
            amount=amount,
            destination=destination,
            cancel_after=cancel_after,
            finish_after=finish_after,
            condition=condition,
            source_tag=source_tag,
            destination_tag=destination_tag
        )
        print(escrow_create)  # the unsigned transaction
        print(escrow_create.is_valid())
        # escrow_create_signed = safe_sign_and_autofill_transaction(escrow_create, self.wallet, self.client)
        # print(escrow_create_signed)  # the signed transaction
        tx_response = submit_and_wait(escrow_create, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def escrow_finish(self, owner_address, offer_sequence, condition, fulfillment):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        escrow_finish = EscrowFinish(
            account=self.wallet.classic_address,
            owner=owner_address,
            offer_sequence=offer_sequence,
            condition=condition,
            fulfillment=fulfillment
        )
        print(escrow_finish)  # the unsigned transaction
        print(escrow_finish.is_valid())
        # escrow_finish_signed = safe_sign_and_autofill_transaction(escrow_finish, self.wallet, self.client)
        # print(escrow_finish_signed)  # the signed transaction
        tx_response = submit_and_wait(escrow_finish, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def offer_cancel(self, offer_sequence):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        offer_cancel = OfferCancel(
            account=self.wallet.classic_address, offer_sequence=offer_sequence)
        print(offer_cancel)  # the unsigned transaction
        print(offer_cancel.is_valid())
        # offer_cancel_signed = safe_sign_and_autofill_transaction(offer_cancel, self.wallet, self.client)
        # print(offer_cancel_signed)  # the signed transaction
        tx_response = submit_and_wait(offer_cancel, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def set_regular_key(self, regular_key):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        set_regular_key = SetRegularKey(
            account=self.wallet.classic_address, regular_key=regular_key)
        print(set_regular_key)  # the unsigned transaction
        print(set_regular_key.is_valid())
        # set_regular_key_signed = safe_sign_and_autofill_transaction(set_regular_key, self.wallet, self.client)
        # print(set_regular_key_signed)  # the signed transaction
        tx_response = submit_and_wait(
            set_regular_key, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def trust_set(self, currency, limit, quality_in=None, quality_out=None):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        trust_set = TrustSet(
            account=self.wallet.classic_address,
            limit=limit,
            currency=currency,
            quality_in=quality_in,
            quality_out=quality_out
        )
        print(trust_set)  # the unsigned transaction
        print(trust_set.is_valid())
        # trust_set_signed = safe_sign_and_autofill_transaction(trust_set, self.wallet, self.client)
        # print(trust_set_signed)  # the signed transaction
        tx_response = submit_and_wait(trust_set, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def set_fee(self, base_fee, reference_fee_units):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        set_fee = SetFee(
            account=self.wallet.classic_address,
            base_fee=base_fee,
            reference_fee_units=reference_fee_units
        )
        print(set_fee)  # the unsigned transaction
        print(set_fee.is_valid())
        # set_fee_signed = safe_sign_and_autofill_transaction(set_fee, self.wallet, self.client)
        # print(set_fee_signed)  # the signed transaction
        tx_response = submit_and_wait(set_fee, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def signer_list_set(self, signer_quorum, signer_entries):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        signer_list_set = SignerListSet(
            account=self.wallet.classic_address,
            signer_quorum=signer_quorum,
            signer_entries=signer_entries
        )
        print(signer_list_set)  # the unsigned transaction
        print(signer_list_set.is_valid())
        # signer_list_set_signed = safe_sign_and_autofill_transaction(signer_list_set, self.wallet, self.client)
        # print(signer_list_set_signed)  # the signed transaction
        tx_response = submit_and_wait(signer_list, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def deposit_preauth(self, authorized_address, destination):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        deposit_preauth = DepositPreauth(
            account=self.wallet.classic_address,
            authorized_address=authorized_address,
            destination=destination
        )
        print(deposit_preauth)  # the unsigned transaction
        print(deposit_preauth.is_valid())
        # deposit_preauth_signed = safe_sign_and_autofill_transaction(deposit_preauth, self.wallet, self.client)
        # print(deposit_preauth_signed)  # the signed transaction
        tx_response = submit_and_wait(
            deposit_preauth, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def check_cancel(self, check_id):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        check_cancel = CheckCancel(
            account=self.wallet.classic_address, check_id=check_id)
        print(check_cancel)  # the unsigned transaction
        print(check_cancel.is_valid())
        # check_cancel_signed = safe_sign_and_autofill_transaction(check_cancel, self.wallet, self.client)
        # print(check_cancel_signed)  # the signed transaction
        tx_response = submit_and_wait(
            check_cancel_signed, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def check_cash(self, check_id, amount):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        check_cash = CheckCash(
            account=self.wallet.classic_address, check_id=check_id, amount=amount)
        print(check_cash)  # the unsigned transaction
        print(check_cash.is_valid())
        # check_cash_signed = safe_sign_and_autofill_transaction(check_cash, self.wallet, self.client)
        # print(check_cash_signed)  # the signed transaction
        tx_response = submit_and_wait(check_cash, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def check_create(self, destination, send_max, expiration):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        check_create = CheckCreate(
            account=self.wallet.classic_address,
            destination=destination,
            send_max=send_max,
            expiration=expiration
        )
        print(check_create)  # the unsigned transaction
        print(check_create.is_valid())
        # check_create_signed = safe_sign_and_autofill_transaction(check_create, self.wallet, self.client)
        # print(check_create_signed)  # the signed transaction
        tx_response = submit_and_wait(check_create, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def escrow_cancel(self, offer_sequence, owner, offer_sequence_close):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        escrow_cancel = EscrowCancel(
            account=self.wallet.classic_address,
            offer_sequence=offer_sequence,
            owner=owner,
            offer_sequence_close=offer_sequence_close
        )
        print(escrow_cancel)  # the unsigned transaction
        print(escrow_cancel.is_valid())
        # escrow_cancel_signed = safe_sign_and_autofill_transaction(escrow_cancel, self.wallet, self.client)
        # print(escrow_cancel_signed)  # the signed transaction
        tx_response = submit_and_wait(escrow_cancel, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def account_set(self, transfer_rate=None, domain=None, tick_size=None, set_flag=None, clear_flag=None):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        account_set = AccountSet(
            account=self.wallet.classic_address,
            transfer_rate=transfer_rate,
            domain=domain,
            tick_size=tick_size,
            set_flag=set_flag,
            clear_flag=clear_flag
        )
        print(account_set)  # the unsigned transaction
        print(account_set.is_valid())
        # account_set_signed = safe_sign_and_autofill_transaction(account_set, self.wallet, self.client)
        # print(account_set_signed)  # the signed transaction
        tx_response = submit_and_wait(account_set, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def escrow_finish(self, owner_address, offer_sequence, condition, fulfillment):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        escrow_finish = EscrowFinish(
            account=self.wallet.classic_address,
            owner=owner_address,
            offer_sequence=offer_sequence,
            condition=condition,
            fulfillment=fulfillment
        )
        print(escrow_finish)  # the unsigned transaction
        print(escrow_finish.is_valid())
        # escrow_finish_signed = safe_sign_and_autofill_transaction(escrow_finish, self.wallet, self.client)
        # print(escrow_finish_signed)  # the signed transaction
        tx_response = submit_and_wait(escrow_finish, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def offer_create(self, taker_pays, taker_gets, expiration, offer_sequence=None):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        offer_create = OfferCreate(
            account=self.wallet.classic_address,
            taker_pays=taker_pays,
            taker_gets=taker_gets,
            expiration=expiration,
            offer_sequence=offer_sequence
        )
        print(offer_create)  # the unsigned transaction
        print(offer_create.is_valid())
        # offer_create_signed = safe_sign_and_autofill_transaction(offer_create, self.wallet, self.client)
        # print(offer_create_signed)  # the signed transaction
        tx_response = submit_and_wait(offer_create, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def payment_channel_claim(self, channel, amount, signature):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        payment_channel_claim = PaymentChannelClaim(
            account=self.wallet.classic_address,
            channel=channel,
            amount=amount,
            signature=signature
        )
        print(payment_channel_claim)  # the unsigned transaction
        print(payment_channel_claim.is_valid())
        # payment_channel_claim_signed = safe_sign_and_autofill_transaction(payment_channel_claim, self.wallet, self.client)
        # print(payment_channel_claim_signed)  # the signed transaction
        tx_response = submit_and_wait(
            payment_channel_claim, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def payment_channel_create(self, destination, amount, settle_delay, public_key, cancel_after=None, destination_tag=None):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        payment_channel_create = PaymentChannelCreate(
            account=self.wallet.classic_address,
            destination=destination,
            amount=amount,
            settle_delay=settle_delay,
            public_key=public_key,
            cancel_after=cancel_after,
            destination_tag=destination_tag
        )
        print(payment_channel_create)  # the unsigned transaction
        print(payment_channel_create.is_valid())
        # payment_channel_create_signed = safe_sign_and_autofill_transaction(payment_channel_create, self.wallet, self.client)
        # print(payment_channel_create_signed)  # the signed transaction
        tx_response = submit_and_wait(
            payment_channel_create, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def payment_channel_fund(self, channel, amount):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        payment_channel_fund = PaymentChannelFund(
            account=self.wallet.classic_address,
            channel=channel,
            amount=amount
        )
        print(payment_channel_fund)  # the unsigned transaction
        print(payment_channel_fund.is_valid())
        # payment_channel_fund_signed = safe_sign_and_autofill_transaction(payment_channel_fund, self.wallet, self.client)
        # print(payment_channel_fund_signed)  # the signed transaction
        tx_response = submit_and_wait(
            payment_channel_fund, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))

    @classmethod
    def ticket_create(self, ticket_count, destination, expiration):
        current_validated_ledger = get_latest_validated_ledger_sequence(
            self.client)
        self.wallet.sequence = get_next_valid_seq_number(
            self.wallet.classic_address, self.client)
        ticket_create = TicketCreate(
            account=self.wallet.classic_address,
            ticket_count=ticket_count,
            destination=destination,
            expiration=expiration
        )
        print(ticket_create)  # the unsigned transaction
        print(ticket_create.is_valid())
        # ticket_create_signed = safe_sign_and_autofill_transaction(ticket_create, self.wallet, self.client)
        # print(ticket_create_signed)  # the signed transaction
        tx_response = submit_and_wait(ticket_create, self.client, self.wallet)
        print("response.status: ", tx_response.status)
        print(json.dumps(tx_response.result, indent=4, sort_keys=True))


# main function, entrypoint
if __name__ == "__main__":
    # cli parser and option handling
    parser = argparse.ArgumentParser(
        description="A command-line interface for working with the XRPL")
    parser.add_argument("-b", "--brainwallet",
                        help="use a brain wallet passphrase")
    parser.add_argument("-a", "--account", help="classic account address")
    parser.add_argument("-s", "--secret", help="seed key")
    parser.add_argument("-pay", "--payment", help="send payment of amount")
    parser.add_argument("-tag", "--tag", help="optional tag for payment")
    parser.add_argument("-d", "--destination",
                        help="destination wallet for transaction")
    parser.add_argument("-g", "--generate_wallet",
                        help="generate a wallet from faucet", nargs='?', const=1)
    parser.add_argument(
        "-rm", "--delete", help="delete wallet and send balance to destination", nargs='?')
    parser.add_argument("-l", "--listnft",
                        help="list nft's on account", nargs='?', const=1)
    parser.add_argument("-t", "--tokenurl", help="mint a NFT token url")
    parser.add_argument("-f", "--flags", help="NFT flags")
    parser.add_argument("-i", "--tokenid", help="token id")
    parser.add_argument("-m", "--amount", help="amount")
    parser.add_argument("-x", "--tokenofferindex", help="tokenofferindex")
    parser.add_argument("-o", "--owner", help="owner")
    parser.add_argument("-n", "--network",
                        help="use with list for server list")
    args = parser.parse_args()
    # create the XRPL object
    xrplobj = XRPLobject()
    # configure network node for interaction with XRPL
    if str(args.network) == "list":
        print("0 = main, 1 = testnet, 2 = devnet, 3 = ammdev, 4 = local")
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
            XRPLobject.server = str(networks["ammdev"][1]["jsonrpc"])
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
            xrplobj.payment(args.destination, args.payment, int(args.tag))
        elif args.destination and not args.tag:
            xrplobj.payment(args.destination, args.payment, None)
        else:
            print("Not enough parameters for payment, check your command")
    # default get account details
    if xrplobj.account:
        xrplobj.getaccount()
        sys.exit(0)
