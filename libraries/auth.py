import requests
import os
import urllib


class Authentication:
    def __init__(self):
        self.__url__ = os.environ.get('API_URL')
        self.__token__ = None

    def login(self):
        url = f"{self.__url__}/auth"
        username = urllib.parse.quote(os.environ.get('API_USERNAME'))
        password = urllib.parse.quote(os.environ.get('API_PASSWORD'))
        payload = f'email={username}&password={password}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        r = response.json()
        self.__token__ = r['data']['token']
        print(response.text)

    def logout(self):
        url = f"{self.__url__}/auth/logout"

        payload = {}
        headers = {
            'Authorization': f'Bearer {self.__token__}'}

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    def create_interesting(self, asset='KUB', exchange='Bitkub', quote='THB', trend='-', price=0, percent=0):
        url = f"{self.__url__}/interesting/create"

        payload = f'asset_id={asset}&exchange_id={exchange}&currency_id={quote}&trend={trend}&last_price={price}&last_percent={percent}'
        headers = {
            'Authorization': f'Bearer {self.__token__}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
