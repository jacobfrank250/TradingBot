# TradingBot
An automated Coinbase Pro trading bot built in Python.

The bot uses a simple exponential moving average (EMA) crossover strategy to attempt to profit from short-term upwards trends in cryptocurrency. A buy/sell signal is triggered when the 5-period EMA and the 20-period EMA intercept. The bot uses the Coinbase Pro platform to buy/sell cryptocurrency, accessed via the official API.

The exit strategy of the bot is straightforward. Once a buy order has been fulfilled, the bot waits for either the price to change +40 basis points or for the EMAs to intercept. The first event to occur triggers the bot to sell the position.

The bot creates orders that only provide liquidity to the market and thus are market 'maker' orders. The significance of this is that Coinbase Pro currently charges 0% on fees for 'maker' orders.

The project uses Threads to perform separate functions:
*  Grab live price, calculate EMAs and identify if a crossover has occurred
*  Perform a trading action - buy/sell depending on crossover

As the bot runs, all prices and transactions are logged into separate MongoDB collections.

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
* [CBPro Python Client](https://github.com/danpaquin/coinbasepro-python)


