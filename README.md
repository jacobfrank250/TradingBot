# Coinbase Pro Trading Bot

The bot uses an exponential moving average (EMA) crossover trade strategy. It chooses to buy/sell when the 5-period EMA and the 20-period EMA intercept. 

The bot uses the Coinbase Pro's REST API to perform transactions, and determines the price to buy/sell at by maintaing the live order book through Coinbase Pro's Websocket. 

The program uses separate threads to:
*  Track live price and maintain a snapshot of the full orderbook
*  Calculate EMAs and identify if a crossover has occurred
*  Buy/sell depending on crossover

As the bot runs, all prices and transactions are logged into MongoDB collections.

## Getting Started

These instructions allow you to get running and customize the project.

### Prerequisites

You will need a Coinbase Pro account/API key and a MongoDB account.
Create a config file (config.py) in the root directory with the following format:

```
API_KEY = ""
API_SECRET = ""
API_PASS = ""
API_URL = "https://api-public.sandbox.pro.coinbase.com/"

MONGO_USER = ""
MONGO_PASS = ""
```

### How To Run Program

Navigate to project directory and enter
```
python TradeBot.py
```

## Acknowledgments
* [Coinbase Pro Documentation](https://docs.pro.coinbase.com/#introduction)
* [GDAX Trading Bot](https://github.com/calum-mcg/gdax-tradingbot)


