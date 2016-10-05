import random

class Strategy(object):
    def __init__(self, max_capital_risk=3., pairs=['EUR_USD']):
        self.max_capital_risk = max_capital_risk

    def action(self, candles):
        pass

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

class ParabolicSAR(Strategy):
    def __init__(self, **kwargs):
        super(ParabolicSAR, self).__init__(**kwargs)
        self.buy = False

    def action(self, candles):
        self.buy = not self.buy

        return 'buy' if self.buy else 'sell'