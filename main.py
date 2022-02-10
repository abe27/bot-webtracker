import os
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

# init
load_dotenv()
api_key = os.environ.get('BINANCE_API_KEY')
api_secret = os.environ.get('BINANCE_API_SECRET')


def main():
    client = Client(api_key, api_secret)
    balance = client.get_account()
    i = 0
    while i < len(balance['balances']):
        r = balance['balances'][i]
        if str(r['asset']).find('LD') < 0:
            print(f"{(i + 1)}. ==> {r}")

        i += 1

    client.close_connection()


if __name__ == '__main__':
    main()
    sys.exit(0)
