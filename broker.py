import requests
import json
from datetime import datetime

class API(object):
    """API provides a wrapper for the Oanda REST API
    Allows basic trading functionality such as retrieving market data,
    placing orders etc.
    """
    def __init__(self, account_id, access_token, type = 'practice'):

        if type == 'practice':
            self.domain = 'https://api-fxpractice.oanda.com'

        self.account_id = account_id
        self.access_token = access_token
        self.client = requests.Session()

        self.headers = self.client.headers
        self.headers['Authorization'] = 'Bearer ' + self.access_token

    """Prices"""

    def get_prices(self, *args):
        params = {'instruments': ','.join(args)}
        return self.request('get', 'v1/prices', **params)['prices']

    def get_history(self, instrument, period='D', count=100):
        params = {
            'instrument': instrument,
            'granularity': period,
            'count': count
        }

        return self.request('get', 'v1/candles', **params)

    """Orders"""

    def get_orders(self, **params):
        return self.request('get', 'v1/accounts/{}/orders'.format(self.account_id))['orders']

    def place_order(self, instrument, units, side, type, take_profit = 0, stop_loss = 0, trailing_stop = 0):
        data = {'instrument': instrument,
                'units': units,
                'side': side,
                'type': type,
                'take_profit': take_profit,
                'stop_loss': stop_loss,
                'trailing_stop': trailing_stop,
                }

        return self.request('post', 'v1/accounts/{}/orders'.format(self.account_id), **data)

    """Trades"""

    def get_trades(self):
        return self.request('get', 'v1/accounts/{}/trades'.format(self.account_id))['trades']

    def close_trades(self, *args):
        args = map(str, args)
        return self.request('delete', 'v1/accounts/{}/trades/{}'.format(self.account_id, ','.join(args)))

    """Positions"""

    def get_positions(self):
        return self.request('get', 'v1/accounts/{}/positions'.format(self.account_id))['positions']

    def close_position(self, pair):
        return self.request('delete', 'v1/accounts/{}/positions/{}'.format(self.account_id, pair))

    def close_all_positions(self):
        for position in self.get_positions():
            self.close_position(position['instrument'])

    """Request"""

    def request(self, method, endpoint, **params):
        url = '{}/{}'.format(self.domain, endpoint)
        method = method.lower()

        req = getattr(self.client, method)

        req_args = {}
        if method == 'get':
            req_args['params'] = params
        elif method == 'post' or method == 'delete':
            req_args['data'] = params
        else:
            raise Exception('Bad request type.')

        response = req(url, **req_args)

        return json.loads(response.content.decode('utf-8'), encoding='utf-8')