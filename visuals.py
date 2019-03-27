import matplotlib.pyplot as plt
import pymongo
import bson.json_util as json_util
import json
import numpy as np

pairs =  ['ethbtc', 'xrpbtc', 'bchbtc', 'ltcbtc', 'etcbtc', 'eosbtc', 'adabtc', 'zecbtc', 'omgbtc',
                        'dashbtc', 'trxbtc', 'ontbtc', 'bttbtc', 'iostbtc', 'zilbtc', 'btmbtc', 'elabtc', 'neobtc',
                        'qtumbtc', 'nasbtc', 'elfbtc', 'hcbtc', 'bsvbtc']



db = pymongo.MongoClient('localhost',27017)
db = db['cryptowatch']
col = db['arbitrage']
res = col.find({'market':{'$exists':True}})
res = json_util.dumps(res)
res = json.loads(res)
markets = []
for i in res:

    if i['market'] not in markets:
        markets.append(i['market'])

market_position = {}
for i in range( len(markets) ):
    market_position[markets[i]] = i


for i in pairs:
    res = col.find({'pair':i})
    res = json_util.dumps(res)
    res = json.loads(res)
    means = np.zeros(len(markets) )
    how_many = np.zeros(len(markets) )
    for i in range(len(res)):
        means[ market_position[res[i]['market']] ] += float(res[i]['arbitrage'])
        how_many[ market_position[res[i]['market']] ] += 1
    for i in range(means.shape[0]):
        if how_many[i]==0:
            means[i] = 0
        else:
            means[i] /= how_many[i]
    n , bins, batches = plt.hist(means,bins='auto',label=markets, color='#0504aa')

    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(i)
    #plt.text(23, 45, r'$\mu=15, b=3$')
    #maxfreq = n.max()
    # Set a clean upper y-axis limit.
    #plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.show()

