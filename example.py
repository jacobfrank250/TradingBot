if __name__ == "__main__":
    import sys
    # import cbpro
    import exchange.websocket_client as websock
    import time
    import json
    from config import *
    import pymongo
    from pymongo import MongoClient
    
    #import tick



    # class MyWebsocketClient(cbpro.WebsocketClient):
    class MyWebsocketClient(websock.WebsocketClient):

        def on_open(self):
            self.url = "wss://ws-feed.pro.coinbase.com/"
            # self.products = ["BTC-USD", "ETH-USD"]
            self.products = ["BTC-EUR"]

            #self.channels = ["ticker"]
            
            self.api_key = API_KEY
            self.api_passphrase = API_PASS
            self.api_secret = API_SECRET
            
            self.message_count = 0
            print("Let's count the messages!")
        
        """Note that with the exception of errors, every other message triggers this method including things like subscription
        confirmations. Your code should be prepared to handle unexpected messages.
        """
        def on_message(self, msg):
            #Version 1
            # print(json.dumps(msg, indent=4, sort_keys=True))

            # Version 2
            if 'price' in msg and 'type' in msg:
                print ("Message type:", msg["type"],"\t@ {:.3f}".format(float(msg["price"])))
                self.mongo_price_collection.insert_one(msg)
            # else:
            #     print('prince and type were not in msg')
            #     print(json.dumps(msg, indent=4, sort_keys=True))
            self.message_count += 1

            
        def on_close(self):
            print("-- Goodbye! --")

    
    #connect to a local, running Mongo instance
    mongo_client = MongoClient("mongodb+srv://{}:{}@cluster0-xog0f.mongodb.net/test?retryWrites=true&w=majority".format(MONGO_USER,MONGO_PASS))

    # specify the database and collection
    # db = mongo_client.cryptocurrency_database
    # BTC_collection = db.BTC_collection
    db = mongo_client["cryptocurrency_db"]
    BTC_collection = db["BTC_collection"]


    wsClient = MyWebsocketClient(channels = ["ticker"], mongo_price_collection=BTC_collection) #The ticker channel provides real-time price updates every time a match happens
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