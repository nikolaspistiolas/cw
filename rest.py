import requests
import pymongo


mongo = pymongo.MongoClient('localhost',27017)
db = mongo['cryptowatch']
col = db['arbitrage']
col.insert_one({})
print('ok')
pairs =  ['ethbtc', 'xrpbtc', 'bchbtc', 'ltcbtc', 'etcbtc', 'eosbtc', 'adabtc', 'zecbtc', 'omgbtc',
                        'dashbtc', 'trxbtc', 'ontbtc', 'bttbtc', 'iostbtc', 'zilbtc', 'btmbtc', 'elabtc', 'neobtc',
                        'qtumbtc', 'nasbtc', 'elfbtc', 'hcbtc', 'bsvbtc']
w=0
while(True):

    a = requests.get('https://api.cryptowat.ch/markets/summaries').json()['result']
    keys = a.keys()
    markets = []
    for i in keys:
        market, pair = i.split(':')
        if market not in markets:
            markets.append(market)
    for i in pairs:
        huobi_price = float(a['huobi:'+i]['price']['last'])
        for k in markets:
            if k+ ':' + i in keys:
                market_price = float(a[k+ ':' + i]['price']['last'])
                if market_price != 0:
                    arb = (huobi_price - market_price )/ market_price *100
                    if arb >0 and arb < 20:
                        db_result = { 'market': k, 'pair': i, 'arbitrage': arb}
                        col.insert_one(db_result)
    print(w)
    w = w + 1