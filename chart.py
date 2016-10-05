from matplotlib.finance import candlestick2
import matplotlib.pyplot as plt
from datetime import datetime

def candlestick(candles, price_type = 'ask'):
    price_type = price_type.title()
    quotes = {'open': [], 'high': [], 'low': [], 'close': []}

    for candle in candles:
        quotes['open'].append(candle['openAsk'])
        quotes['high'].append(candle['highAsk'])
        quotes['low'].append(candle['lowAsk'])
        quotes['close'].append(candle['closeAsk'])

    fig, ax = plt.subplots()
    candlestick2(ax, quotes['open'], quotes['close'], quotes['high'], quotes['low'], width=0.5)
    plt.show()