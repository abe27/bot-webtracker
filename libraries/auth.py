import requests
import os
import urllib


class Authentication:
    def __init__(self):
        self.__url__ = os.environ.get('API_URL')
        self.__token__ = None

    def login(self):
        url = f"{self.__url__}/login"
        username = urllib.parse.quote(os.environ.get('API_USERNAME'))
        password = urllib.parse.quote(os.environ.get('API_PASSWORD'))
        payload = f'email={username}&password={password}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        r = response.json()
        self.__token__ = r['data']['token']
        return response.json()

    def logout(self):
        url = f"{self.__url__}/logout"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.__token__}'}

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()

    def create_trend(self, asset='KUB', exchange='Bitkub', quote='THB', trend='-', price=0, percent=0):
        url = f"{self.__url__}/trend/create"

        payload = f'asset_id={asset}&exchange_id={exchange}&currency_id={quote}&trend={trend}&last_price={price}&last_percent={percent}'
        headers = {
            'Authorization': f'Bearer {self.__token__}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()

    def create_trend_with_timeframe(self, asset='BTC', currency='THB', on_time='4h', trend='LONG'):
        url = f"{self.__url__}/trend/timeframe"

        payload = f'asset={asset}&currency={currency}&on_time={on_time}&trend={trend}'
        headers = {
            'Authorization': f'Bearer {self.__token__}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # print(response.text)
        return response.json()

    def create_order(self, trend_id,
                     order_type_id='spot',
                     orderno=None,
                     hashno=None,
                     price=0,
                     total_coin=0,
                     fee=0,
                     trend='Buy',
                     type='Auto',
                     status='Limit',
                     is_active=1):
        url = f"{self.__url__}/order/create"

        payload = f'trend_id={trend_id}&order_type_id={order_type_id}&orderno={orderno}&hashno={hashno}&price={price}&total_coin={total_coin}&fee={fee}&trend={trend}&type={type}&status={status}&is_active={is_active}'
        headers = {
            'Authorization': f'Bearer {self.__token__}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
