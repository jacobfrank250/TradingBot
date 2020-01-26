
from pymongo import MongoClient
from model.WebsocketThread import *

#connect to a local, running Mongo instance
mongo_client = MongoClient("mongodb+srv://{}:{}@cluster0-xog0f.mongodb.net/test?retryWrites=true&w=majority".format(MONGO_USER,MONGO_PASS))

# specify the database and collection
# db = mongo_client.cryptocurrency_database
# BTC_collection = db.BTC_collection
db = mongo_client["cryptocurrency_db"]
BTC_collection = db["BTC_collection"]


# wsClient = WebsocketThread(channels = ["ticker"], mongo_collection=BTC_collection) #The ticker channel provides real-time price updates every time a match happens
# wsClient = WebsocketThread("BTC","EUR",channels = ["ticker"],mongo_collection=BTC_collection) #The ticker channel provides real-time price updates every time a match happens
wsClient = WebsocketThread("BTC","EUR",mongo_collection=BTC_collection,channels=["ticker"]) #The ticker channel provides real-time price updates every time a match happens

wsClient.start()


print(wsClient.url, wsClient.products)
try:
    while True:
        #print("\nMessageCount =", "%i \n" % wsClient.message_count)
        time.sleep(1)
except KeyboardInterrupt:
    wsClient.close()

if wsClient.error:
    sys.exit(1)
else:
    sys.exit(0)