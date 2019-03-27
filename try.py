import pymongo
import bson.json_util as bson
import json

db = pymongo.MongoClient('localhost',27017)
db = db['cryptowatch']
col = db['arbitrage']

res = col.find({'arbitrage':{'$gt':0.7}})
res = bson.dumps(res)

res = json.loads(res)
for i in res:
    print(i)