import random
import numpy as np

class Strategy(object):
    def __init__(self, **kwargs):
        pass

    def action(self, candles):
        pass

    def extract_prices(self, candles, price_type = 'ask'):
        price_type = price_type.capitalize()

        opens = []
        closes = []
        highs = []
        lows = []

        for candle in candles:
            opens.append(candle['open' + price_type])
            closes.append(candle['close' + price_type])
            highs.append(candle['high' + price_type])
            lows.append(candle['high' + price_type])

        return opens, closes, highs, lows

class Random(Strategy):
    def __init__(self, **kwargs):
        super(Random, self).__init__(**kwargs)

    def action(self, candles):
        dice = random.random()

        if dice < 1./3:
            return 'buy'
        elif dice < 2./3:
            return 'sell'
        else:
            return None

class MACD(Strategy):
    def __init__(self, **kwargs):
        super(MACD, self).__init__(**kwargs)
        self.fast_ma_period = kwargs.get('fast_ma_period', 9)
        self.slow_ma_period = kwargs.get('slow_ma_period', 21)

    def construct_ma(self, candles, price_type = 'ask'):
        prices = np.array(self.extract_prices(candles, price_type=price_type)[1], dtype=float)

        length = len(candles)

        slow_ma = np.array([None]*length, dtype=float)
        fast_ma = np.array([None]*length, dtype=float)

        ret = np.cumsum(prices, dtype=float)

        n = self.fast_ma_period
        fast_ma[n:] = ret[n:] - ret[:-n]
        fast_ma /= n
        n = self.slow_ma_period
        slow_ma[n:] = ret[n:] - ret[:-n]
        slow_ma /= n

        return fast_ma, slow_ma

    def action(self, candles):
        fma_ask, sma_ask = self.construct_ma(candles, price_type='ask')
        fma_bid, sma_bid = self.construct_ma(candles, price_type='bid')

        if fma_ask[-1] > sma_ask[-1]:
            return 'buy'
        elif fma_bid[-1] < sma_bid[-1]:
            return 'sell'
        else:
            return 'hold'

class ParabolicSAR(Strategy):
    def __init__(self, **kwargs):
        super(ParabolicSAR, self).__init__(**kwargs)

        self.start = kwargs.get('start', 0.02)
        self.increment = kwargs.get('increment', 0.02)
        self.max_increment = kwargs.get('max_increment', 0.2)

    def construct_psar(self, candles, price_type = 'ask'):
        price_type = price_type.title()

        opens, closes, highs, lows = self.extract_prices(candles, price_type)

        length = len(candles)
        af = self.start
        inc = self.increment
        uptrend = True
        psar = closes[:]
        psar_uptrend = [None]*length
        psar_downtrend = [None]*length

        high_point = highs[0]
        low_point = lows[0]

        for i in xrange(2, length):
            if uptrend:
                psar[i] = psar[i - 1] + af*(high_point - psar[i - 1])
            else:
                psar[i] = psar[i - 1] + af*(low_point - psar[i - 1])

            reverse = False

            if uptrend:
                if lows[i] < psar[i]:
                    uptrend = False
                    reverse = True
                    psar[i] = high_point
                    low_point = lows[i]
                    af = self.start

            else:
                if highs[i] > psar[i]:
                    uptrend = True
                    reverse = True
                    psar[i] = low_point
                    high_point = highs[i]
                    af = self.start

            if not reverse:
                if uptrend:
                    if highs[i] > high_point:
                        high_point = highs[i]
                        af = min(af + inc, self.max_increment)

                    if lows[i - 1] < psar[i]:
                        psar[i] = lows[i - 1]

                    if lows[i - 2] < psar[i]:
                        psar[i] = lows[i - 2]

                else:
                    if lows[i] < low_point:
                        low_point = lows[i]
                        af = min(af + inc, self.max_increment)
                    if highs[i - 1] > psar[i]:
                        psar[i] = highs[i - 1]
                    if highs[i - 2] > psar[i]:
                        psar[i] = highs[i - 2]

            if uptrend:
                psar_uptrend[i] = psar[i]
            else:
                psar_downtrend[i] = psar[i]

        return psar_uptrend, psar_downtrend

    def action(self, candles):
        psar_uptrend, psar_downtrend = self.construct_psar(candles, 'ask')

        psar_uptrend = psar_uptrend[-3:]
        psar_downtrend = psar_downtrend[-3:]

        if not None in psar_uptrend:
            return 'buy'
        elif not None in psar_downtrend:
            return 'sell'

        return 'hold'

