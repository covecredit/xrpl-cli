# Notes

These are developer notes and are raw verbatim and may mean something completely different than expected.

# Build Platform

Developers seeking to make the most out of Linux development on XRPL should use Ubuntu 20.04 LTS. Tested
a number of different Linux OS and non-Ubuntu / Debian / Redhat(?) / CentOS distributions do not have all
the available Next.JS modules for compiling XUMM. If you intend to build a full xApp experience then stick
to the upstream developers preferred build which for XUMM and all tested XRPLF repos builds easily on
Ubuntu. If you build on Arch Linux for instance, it will require patches to the build processes and to 
leverage the UI/UX code being used for Linux.

# Steps for developers

1. build rippled and configure with xrpl-node-configurator 
2. "pip3 install -r requirements.txt"
3. python3 xrpl-cli.py --help  

# OpenSSL ripemd160 support on Ubuntu

OpenSSL .cnf file should enable legacy support for ripemd160 (note this is insecure) as xrpl-py
uses hashlib which supports ripemd160 but if the host is using recent OpenSSL then it will be disabled.
Add config file similar to the following to activate the legacy providers in the SSL backend.

```` 
# List of providers to load
[provider_sect]
default = default_sect
legacy = legacy_sect
# The fips section name should match the section name inside the
# included fipsmodule.cnf.
# fips = fips_sect

# If no providers are activated explicitly, the default one is activated implicitly.
# See man 7 OSSL_PROVIDER-default for more details.
#
# If you add a section explicitly activating any other provider(s), you most
# probably need to explicitly activate the default provider, otherwise it
# becomes unavailable in openssl.  As a consequence applications depending on
# OpenSSL may not work correctly which could lead to significant system
# problems including inability to remotely access the system.
[default_sect]
activate = 1
[legacy_sect]
activate = 1 
````

# RPC notes
// RPC handler table
static HandlerTable handlerTable{
    {"account_channels", &doAccountChannels, LimitRange{10, 50, 256}},
    {"account_currencies", &doAccountCurrencies, {}},
    {"account_info", &doAccountInfo, {}},
    {"account_lines", &doAccountLines, LimitRange{10, 50, 256}},
    {"account_nfts", &doAccountNFTs, LimitRange{1, 5, 10}},
    {"account_objects", &doAccountObjects, LimitRange{10, 50, 256}},
    {"account_offers", &doAccountOffers, LimitRange{10, 50, 256}},
    {"account_tx", &doAccountTx, LimitRange{1, 50, 100}},
    {"gateway_balances", &doGatewayBalances, {}},
    {"noripple_check", &doNoRippleCheck, {}},
    {"book_offers", &doBookOffers, LimitRange{1, 50, 100}},
    {"ledger", &doLedger, {}},
    {"ledger_data", &doLedgerData, LimitRange{1, 100, 2048}},
    {"nft_buy_offers", &doNFTBuyOffers, LimitRange{1, 50, 100}},
    {"nft_info", &doNFTInfo},
    {"nft_sell_offers", &doNFTSellOffers, LimitRange{1, 50, 100}},
    {"ledger_entry", &doLedgerEntry, {}},
    {"ledger_range", &doLedgerRange, {}},
    {"subscribe", &doSubscribe, {}},
    {"server_info", &doServerInfo, {}},
    {"unsubscribe", &doUnsubscribe, {}},
    {"tx", &doTx, {}},
    {"transaction_entry", &doTransactionEntry, {}},
    {"random", &doRandom, {}}};

// commands.js 
server_info / server_state

# Mnemonic Wallets, seeds and XLS-7

The mnemonic brain wallet implementation in xrpl-cli is a python re-write of the rippled implementation. 

# mint.py

This will mint an arbitrary string as the uri on XLS-20 sandbox network and output the account details.

harnesses todo:
* NFTokenAcceptOffer
* NFTokenBurn
* NFTokenCancelOffer
* NFTokenCreateOffer
* NFTokenCreateOfferFlag
* NFTokenCreateOfferFlagInterface
* NFTokenMint
* NFTokenMintFlag
* NFTokenMintFlagInterface


The following are the most commonly used transactions (implement as priority)
* AccountDelete - x
* NFTokenAcceptOffer
* NFTokenCancelOffer
* NFTokenCreateOffer
* NFTokenMint - x (add takon parameter)
* OfferCancel
* OfferCreate
* Payment
* TicketCreate
* TrustSet

