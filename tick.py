from datetime import datetime


class Tick:

    def __init__(self, tick_dict):
        self.product_id = tick_dict['product_id']
        self.best_bid = float(tick_dict['best_bid'])
        self.best_ask = float(tick_dict['best_ask'])
        self.price = float(tick_dict['price'])
        self.side = tick_dict['side']
        self.size = float(tick_dict['last_size'])
        self.time = datetime.strptime(tick_dict['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    
    def spread(self):
        return self.best_ask - self.best_bid

    def __repr__(self):
        rep = "{}\t\t\t\t {}\n".format(self.product_id, self.time)
        rep += "=============================================================\n"
        rep += " Price: ${:.2f}\t Size: {:.8f}\t Side: {: >5}\n".format(self.price, self.size, self.side)
        rep += "Best ask: ${:.2f}\tBest bid: ${:.2f}\tSpread: ${:.2f}\n".format(self.best_ask, self.best_bid, self.spread)
        rep += "=============================================================\n"
        return rep