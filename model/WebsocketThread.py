# if __name__ == "__main__":
import sys
#import exchange.websocket_client.WebsocketClient as cbWebsocketClient
from exchange.websocket_client import WebsocketClient as cbWebsocketClient
import time
import json
from config import *
from exchange.CoinBase import *
# from Functions import *
from model.Functions import *
#import Functions
from threading import Event, Thread
#from pymongo import MongoClient



class WebsocketThread(cbWebsocketClient):
    """Class used to retrieve price from websocket,
        calculate EMA & Crossover 
        and then trigger a separate thread to buy/sell the chosen cryptocurrency
    """
    # def __init__(self, event, wait_time, quote_currency, base_currency):
    # def __init__(self,quote_currency, base_currency):
    # def __init__(self,quote_currency,base_currency,mongo_collection=None,*,channels):
    def __init__(self,quote_currency,base_currency,mongo_price_collection,mongo_transaction_collection,channels):

        # WebsocketThread.__init__(self)
         # inherit the parent--WebsocketClient--init function
        cbWebsocketClient.__init__(self,mongo_price_collection=mongo_price_collection,mongo_transaction_collection = mongo_transaction_collection,channels=channels)
        #self.stopped = event
        #self.wait_time = wait_time
        self.quote_currency = quote_currency
        self.base_currency = base_currency
        #self.channels = channels
        #Authenticate details
        self.CoinBase = CoinbaseExchange(API_KEY, API_SECRET, API_PASS, API_URL)

        #Create model
        # self.model = Model(csv_price, csv_transactions)
        # self.model = Model(self.mongo_collection)
        self.model = Model(self.mongo_price_collection,self.mongo_transaction_collection)


        #Choose Product
        self.product_id = self.CoinBase.getProductId(self.quote_currency, self.base_currency)
        #Specify timeout duration
        self.order_timeout = 900 #15 minutes (in seconds)
        #Display welcome message
        print('Running...')
        #self.CoinBase.getBalance(self.base_currency)

    def on_open(self):
            self.url = "wss://ws-feed.pro.coinbase.com/"
            # self.products = ["BTC-USD", "ETH-USD"]
            self.products = ["BTC-EUR"]

            #self.channels = ["ticker"]
            
            self.api_key = API_KEY
            self.api_passphrase = API_PASS
            self.api_secret = API_SECRET
            
        

            
    def on_close(self):
        print("-- Goodbye! --")
    
     
          
    """Note that with the exception of errors, every other message triggers this method including things like subscription
    confirmations. Your code should be prepared to handle unexpected messages.
    """
    def on_message(self, msg):
       
        # if 'price' in msg and 'type' in msg:
        #     print ("Message type:", msg["type"],"\t@ {:.3f}".format(float(msg["price"])))
        #     self.mongo_collection.insert_one(msg)
       
        # When we receive message from the ticker channel
        if msg['type'] == "ticker":
            if 'price' in msg:
                #self.model.calculateEma(self.CoinBase, msg['price'])
                self.EMACrossover(msg['price'])

    def order(self, type):
        if (type == 'sell'):
            #Sell product
            #Get all open orders and cancel
            open_orders = self.CoinBase.getOrders()
            if(len(open_orders) > 0):
                for order in open_orders:
                    self.CoinBase.cancelOrder(order['id'])

            current_balance = float(self.CoinBase.getBalance(self.quote_currency))
            if current_balance > 0:
            #Sell current position
                doSellLoop = True
                order = self.model.sell(self.product_id, self.CoinBase, self.quote_currency, self.base_currency)
                try:
                    order_time = order['created_at']
                    order_id = order['id']
                    price = order['price']
                    print('Time: {}, Order: Sell, Price:{}, Status: {}'.format(order_time, price, order['status']))
                    timer_count = 0
                except TypeError:
                     # Order most likely = -1 which occurs when order cannnot be made (id not in order)
                    print('type error. Order = ' + str(order))
                    doSellLoop = False 
                # while True:
                while doSellLoop:
                    #Cancel order if timeout
                    if timer_count > self.order_timeout:
                        self.CoinBase.cancelOrder(order_id)
                        time_now = self.CoinBase.getTime()
                        print('Time: {}, Time limit exceeded, order cancelled'.format(time_now))
                        break
                    order_status = self.CoinBase.getOrderStatus(order_id)
                    if(order_status == '404'):
                        print("Order status 404, Order does not exist. Order was probably canceled. Breaking from Loop")
                        break

                   
                    #Return success message if order successful
                    if order_status == 'done':
                        time_now = self.CoinBase.getTime()
                        print('Time: {}, Sell fulfilled at {}'.format(time_now, order['price']))
                        break
                    time.sleep(1)
                    timer_count = timer_count + 1
            else:
                order_time = self.CoinBase.getTime()
                print('Time: {}, Order: Sell, No currency available.'.format(order_time))

        elif (type == 'buy'):
            current_balance = float(self.CoinBase.getBalance(self.base_currency))
            if current_balance > 0:
            #Buy product
                doBuyLoop = True
                order = self.model.buy(self.product_id, self.CoinBase, self.base_currency)
                try:
                    order_time = order['created_at']
                    order_id = order['id']
                    price = order['price']
                    print('Time: {}, Order: Buy, Price:{},  Status: {}'.format(order_time, price, order['status']))
                    timer_count = 0

                except TypeError:
                    # Order most likely = -1 which occurs when order cannnot be made (id not in order)
                    print('type error. Order = ' + str(order))
                    doBuyLoop = False 
                
                # while True:
                while doBuyLoop:
                    #Cancel order if timeout
                    order_status = self.CoinBase.getOrderStatus(order_id)
                    if timer_count > self.order_timeout:
                        self.CoinBase.cancelOrder(order_id)
                        time_now = self.CoinBase.getTime()
                        print('Time: {}, Time limit exceeded, order cancelled'.format(time_now))
                        break
                    elif order_status == 'done':
                        #Return success message if order successful & create sell limit order
                        time_now = self.CoinBase.getTime()
                        print('Time: {}, Buy fulfilled at {}'.format(time_now, order['price']))
                        upper_order = self.model.sellUpper(self.product_id, self.CoinBase, self.quote_currency, order['price'], self.base_currency)
                        try:
                            order_time = upper_order['created_at']
                            order_price = upper_order['price']
                            print('Time:{}, Order: SellUpper, Price:{}, Status: {}'.format(order_time, order_price, order['status']))
                        except TypeError:
                            # Order most likely = -1 which occurs when order cannnot be made (id not in order)
                            print('type error. Order = ' + str(order))
                        break
                    elif(order_status == '404'):
                        print("Order status 404, Order does not exist. Order was probably canceled. Breaking from Loop")
                        break
                    time.sleep(1)
                    timer_count = timer_count + 1
            else:
                order_time = self.CoinBase.getTime()
                print('Time: {}, Order: Buy, No currency available.'.format(order_time))
    
    def EMACrossover(self,price):
        #Trigger order function on separate thread if EMA crossover detected & RSI within threshold
        # self.model.calculateEma(self.CoinBase, self.product_id)
        self.model.calculateEma(self.CoinBase, price)
        self.model.calculateRSI(14)
        signal = self.model.calculateCrossover()
        if signal is not None:
            if signal['value'] == 'buy':
                print("signal value is buy")
                order_thread = Thread(target=self.order, args=('buy',))
                order_thread.daemon = True
                order_thread.start()
            elif signal['value'] == 'sell':
                print("signal value is sell")
                order_thread = Thread(target=self.order, args=('sell',))
                order_thread.daemon = True
                order_thread.start()

    # #connect to a local, running Mongo instance
    # mongo_client = MongoClient("mongodb+srv://{}:{}@cluster0-xog0f.mongodb.net/test?retryWrites=true&w=majority".format(MONGO_USER,MONGO_PASS))

    # # specify the database and collection
    # # db = mongo_client.cryptocurrency_database
    # # BTC_collection = db.BTC_collection
    # db = mongo_client["cryptocurrency_db"]
    # BTC_collection = db["BTC_collection"]


    # # wsClient = WebsocketThread(channels = ["ticker"], mongo_collection=BTC_collection) #The ticker channel provides real-time price updates every time a match happens
    # wsClient = WebsocketThread('BTC','EUR') #The ticker channel provides real-time price updates every time a match happens

    # wsClient.start()
    # print(wsClient.url, wsClient.products)
    # try:
    #     while True:
    #         #print("\nMessageCount =", "%i \n" % wsClient.message_count)
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     wsClient.close()

    # if wsClient.error:
    #     sys.exit(1)
    # else:
    #     sys.exit(0)


        

        

