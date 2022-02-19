import hashlib
import hmac
import os
import json

import requests


def json_encode(data):
    return json.dumps(data, separators=(',', ':'), sort_keys=True)


class BitkubApi:
    def __init__(self):
        # API info
        self.API_HOST = os.environ.get('BITKUB_HOST')
        self.API_KEY = os.environ.get('BITKUB_KEY')
        self.API_SECRET = os.environ.get('BITKUB_SECRET')

        self.header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-BTK-APIKEY': self.API_KEY,
        }

    def sign(self, data):
        j = json_encode(data)
        # print('Signing payload: ' + j)
        h = hmac.new(self.API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
        return h.hexdigest()

    # check server time
    def timeserver(self):
        response = requests.get(self.API_HOST + '/api/servertime')
        ts = int(response.text)
        # print('Server time: ' + response.text)
        return ts

    # get last price
    def get_price(self, name):
        product = name
        ticker = requests.get(self.API_HOST + '/api/market/ticker')
        ticker = ticker.json()
        price = float(ticker[product]['last'])
        return price

    # get order info
    def order_info(self, symbol, orderid, side):
        order_info = {
            'sym': symbol,
            'id': orderid,
            'sd': side,
            'ts': self.timeserver(), }

        signature = self.sign(order_info)
        order_info['sig'] = signature
        r = requests.post(self.API_HOST + '/api/market/order-info', headers=self.header, data=json_encode(order_info))
        return r

    # get my-open-orders
    def my_open_orders(self, symbol):
        open_orders = {
            'sym': symbol,
            'ts': self.timeserver(), }

        signature = self.sign(open_orders)
        open_orders['sig'] = signature
        r = requests.post(self.API_HOST + '/api/market/my-open-orders', headers=self.header, data=json_encode(open_orders))
        return r

    def create_buy(self, symbol, amount, rate, order_type):
        data = {
            'sym': symbol,
            'amt': amount,  # THB จำนวนเงินที่ต้องการซื้อ
            'rat': rate, # THB rate ราคาที่ต้องการ
            'typ': order_type,
            'ts': self.timeserver(), }

        signature = self.sign(data)
        data['sig'] = signature

        # print('Payload with signature: ' + json_encode(data))
        r = requests.post(self.API_HOST + '/api/market/place-bid', headers=self.header, data=json_encode(data))
        print('Response: ' + r.text)
        return r

    def create_sell(self, symbol, amount, rate, order_type):
        data = {
            'sym': symbol,
            'amt': amount,  # THB จำนวนเงินที่ต้องการซื้อ
            'rat': rate, # THB rate ราคาที่ต้องการ
            'typ': order_type,
            'ts': self.timeserver(), }

        signature = self.sign(data)
        data['sig'] = signature

        # print('Payload with signature: ' + json_encode(data))
        r = requests.post(self.API_HOST + '/api/market/place-ask', headers=self.header, data=json_encode(data))
        print('Response: ' + r.text)
        return r





