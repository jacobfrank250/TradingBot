# TradingBot
An automated GDAX trading bot built in Python.

The bot uses a simple exponential moving average (EMA) crossover strategy to attempt to profit from short-term upwards trends in cryptocurrency. A buy/sell signal is triggered when the 5-period EMA and the 20-period EMA intercept. The bot uses the GDAX platform to buy/sell cryptocurrency, accessed via the official API.

The exit strategy of the bot is straightforward. Once a buy order has been fulfilled, the bot waits for either the price to change +40 basis points or for the EMAs to intercept. The first event to occur triggers the bot to sell the position.

The bot creates orders that only provide liquidity to the market and thus are market 'maker' orders. The significance of this is that GDAX currently charges 0% on fees for 'maker' orders<sup>[1](#myfootnote1)</sup>.

The project uses Threads to perform separate functions:
*  Grab live price, calculate EMAs and identify if a crossover has occurred
*  Perform a trading action - buy/sell depending on crossover

As the bot runs, all prices and transactions are logged into separate CSV files.

## Getting Started

These instructions allow you to get running and customize the project.

### Prerequisites

You will need a Coinbase Pro account and an API key. Create a config file (config.py) in the root directory with the following format:

```
API_KEY = ""
API_SECRET = ""
API_PASS = ""
API_URL = "https://api-public.sandbox.pro.coinbase.com/"
```

## Acknowledgments
* [Coinbase Pro Official Documentation](https://docs.pro.coinbase.com/#introduction)
