# Notes

These are developer notes and are raw verbatim and may mean something completely different than expected.


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

