from time import sleep

class Robot(object):
    def __init__(self, session, strategy, max_time=300):
        self.session = session
        self.strategy = strategy
        self.max_time = max_time

    def trade(self):
        time = 0.

        while time < self.max_time:
            prices = self.session.get_history('EUR_USD', period='M1', count=100)

            action = self.strategy.action(prices['candles'])

            if action == 'buy':
                self.session.place_order('EUR_USD', 100, 'buy', 'market')
            elif action == 'sell':
                self.session.place_order('EUR_USD', 100, 'sell', 'market')

            sleep(15)
            time += 5.

        self.session.close_all_positions()

