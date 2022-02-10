import os
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException
from libraries.exports import Exports
from libraries.recommendation import Recommendation
from dotenv import load_dotenv

# init
load_dotenv()
api_key = os.environ.get('BINANCE_API_KEY')
api_secret = os.environ.get('BINANCE_API_SECRET')

export = Exports()
recommendation = Recommendation()


def main():
    client = Client(api_key, api_secret)

    # # get account
    # bal = []
    # balance = client.get_account()
    # i = 0
    # while i < len(balance['balances']):
    #     r = balance['balances'][i]
    #     if str(r['asset']).find('LD') < 0 and float(str(r['free'])) > 0:
    #         print(f"{(i + 1)}. ==> {r}")
    #         bal.append(r)
    #
    #     i += 1
    # export.export_to_json('exports/balance.json', bal)
    #
    #
    # # get all coin
    # bal = []
    # info = client.get_account_snapshot(type='SPOT')
    # snapshotVos = info['snapshotVos']
    # i = 0
    # while i < len(snapshotVos):
    #     assets = snapshotVos[i]['data']['balances']
    #     for r in assets:
    #         print(r)
    #         if r['asset'].find('LD') < 0:
    #             print(r)
    #             bal.append(r)
    #
    #     i += 1
    # export.export_to_json('exports/assets.json', bal)

    # get products
    products = client.get_products()
    i = 0
    while i < len(products['data']):
        r = products['data'][i]
        print(f"{(i + 1)}. {r['b']}/{r['q']}")
        data = recommendation.summary(exchange='BINANCE', symbol=str(r['b']),currency=str(r['q']))
        print(data)
        i += 1

    client.close_connection()


if __name__ == '__main__':
    main()
    sys.exit(0)
