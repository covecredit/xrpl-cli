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

# Mnemonic Wallets, seeds and XLS-7

The mnemonic brain wallet implementation in xrpl-cli is a python re-write of the rippled implementation. 
