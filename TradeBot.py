
from pymongo import MongoClient
from model.WebsocketThread import *

#connect to a local, running Mongo instance
mongo_client = MongoClient("mongodb+srv://{}:{}@cluster0-xog0f.mongodb.net/test?retryWrites=true&w=majority".format(MONGO_USER,MONGO_PASS))

# specify the database and collections
db = mongo_client["cryptocurrency_db"]
price_collection = db["price_collection"]
transaction_collection = db["transaction_collection"]

wsClient = WebsocketThread("BTC","EUR",mongo_price_collection=price_collection,mongo_transaction_collection=transaction_collection, channels=["ticker"]) 

wsClient.start()


print(wsClient.url, wsClient.products)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    wsClient.close()
    

if wsClient.error:
    sys.exit(1)
else:
    sys.exit(0)