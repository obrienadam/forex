from time import sleep

class Robot(object):
    def __init__(self, session, strategy, max_risk_percent=3.):
        self.session = session
        self.strategy = strategy

        self.info = self.session.account_info()

        self.balance = self.info['balance']
        self.account_currency = self.info['accountCurrency']
        self.leverage = 1./self.info['marginRate']

        self.allow_shorts = True
        self.allow_longs = True

        self.session.close_all_positions()

        self.max_risk_percent = max_risk_percent

    def trade(self, pair, period, max_time):
        pair = pair.upper()
        period = period.upper()

        time = 0.
        units = 0
        max_units = 5000

        info = self.session.instruments_info(pair)
        pip_value = info[0]['pip']
        max_trade_units = info[0]['maxTradeUnits']

        print 'pip value: {}, max units: {}'.format(pip_value, max_trade_units)

        while time < max_time:
            prices = self.session.get_history(pair, period=period, count=150)
            action = self.strategy.action(prices['candles'])

            max_trade_value = self.balance*self.max_risk_percent/100.

            if action == 'buy':
                units_to_buy = max_units - units

                if units_to_buy > 0:
                    self.session.place_order(pair, max_units - units, 'buy', 'market')
                    print 'Bought {} units of {}'.format(max_units - units, pair)
                    units = 5000
                else:
                    print 'No action taken.'

            elif action == 'sell':
                units_to_sell = abs(units + max_units)

                if units_to_sell > 0:
                    self.session.place_order(pair, abs(units + max_units), 'sell', 'market')
                    print 'Sold {} units of {}'.format(abs(units + max_units), pair)
                    units = -5000
                else:
                    print 'No action taken'

            elif action == 'hold':
                print 'No action taken.'

            sleep(60)
            time += 60.

        self.session.close_all_positions()

