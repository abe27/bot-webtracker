import os
import sys
import time

from termcolor import colored
from bitkub import Bitkub
from libraries.recommendation import Recommendation, TimeInterval
from libraries.auth import Authentication
from libraries.logs import Logs
from dotenv import load_dotenv

# initialize
load_dotenv()
API_HOST = os.environ.get('BITKUB_HOST')
API_KEY = os.environ.get('BITKUB_KEY')
API_SECRET = os.environ.get('BITKUB_SECRET')

bitkub = Bitkub(API_KEY, API_SECRET)
recommendation = Recommendation()
timeInterval = TimeInterval()
auth = Authentication()
log = Logs()


def main():
    auth.login()
    # bid = bitkub.place_bid(sym='THB_XRP', amt=25, rat=10, typ='limit')
    # __id = None
    # __hash_no = None
    # if bid['error'] == 0:
    #     print(bid['result'])
    #     __id = bid['result']['id']
    #     __hash_no = bid['result']['hash']
    #
    # time.sleep(15)
    # print('check order')
    # check_bid = bitkub.order_info(sym='THB_XRP', id=__id, sd='buy', hash=__hash_no)
    # print(check_bid)
    #
    # time.sleep(5)
    # print('cancel')
    # cancel_order = bitkub.cancel_order(sym='THB_XRP', id=__id, sd=1, hash=__hash_no)
    # print(cancel_order)

    print(f'status: {bitkub.status()}')
    print(f'time server: {bitkub.servertime()}')
    symbol = bitkub.symbols()
    i = 0
    while i < len(symbol['result']):
        r = symbol['result'][i]
        r['info'] = str(r['info'])[len('Thai Baht to '):]
        r['bq'] = r['symbol']
        r['symbol'] = str(r['symbol'])[len('THB_'):]
        ticker = bitkub.ticker(sym=r['bq'])
        on_time_frame = []
        if len(ticker) > 0:
            # print(r)
            # list of time_interval
            list_time_interval = timeInterval.get_interval()
            scores = len(list_time_interval)
            for x in list_time_interval:
                recomm = recommendation.summary(symbol=r['symbol'], quote='THB', interval=x)
                if len(recomm['RECOMMENDATION']) <= 0:
                    recomm['RECOMMENDATION'] = '-'

                text_color = 'magenta'
                if str(recomm['RECOMMENDATION']) == 'STRONG_BUY':
                    scores -= 1
                    text_color = 'blue'

                elif str(recomm['RECOMMENDATION']) == 'BUY':
                    scores -= 1
                    text_color = 'green'

                elif str(recomm['RECOMMENDATION']) == 'STRONG_SELL':
                    text_color = 'red'

                elif str(recomm['RECOMMENDATION']) == 'SELL':
                    text_color = 'yellow'

                elif str(recomm['RECOMMENDATION']) == 'NEUTRAL':
                    scores -= 0.5
                    text_color = 'cyan'

                print(
                    f"{colored(r['symbol'], 'cyan', attrs=['bold'])} on time {colored(x, 'blue')} is {colored(str(recomm['RECOMMENDATION']), text_color)}")

                str_trend = (str(recomm['RECOMMENDATION'])).replace('SELL', 'SHORT')
                on_time_frame.append({
                    'symbol': r['symbol'],
                    'trend': str(str_trend).replace('BUY', 'LONG'),
                    'on_time': x
                })

            percent = ticker[str(r['bq'])]['percentChange']
            print(f"{r['symbol']} score: {scores} percent: {percent}%")
            print(f"-----------------------------")

            txt_trend = 'SHORT'
            if scores < 4:
                txt_trend = 'LONG'

            if scores < 4 and percent < 3:
                txt_trend = 'INTEREST'
                # open order
                print('open order')

            response_trend = auth.create_trend(asset=r['symbol'], trend=txt_trend, price=ticker[str(r['bq'])]['last'],
                                               percent=percent)
            # create trend with timeframe
            h = 0
            while h < len(on_time_frame):
                tframe = on_time_frame[h]
                auth.create_trend_with_timeframe(asset=tframe['symbol'], on_time=tframe['on_time'],
                                                 trend=tframe['trend'])
                h += 1
            # print(on_time_frame)

            if txt_trend == 'INTEREST':
                print(f"open order {response_trend['data']['id']}")
                # # create order bitkub
                bid = bitkub.place_bid(sym='THB_BTC', amt=50, rat=float(ticker[str(r['bq'])]['last']) - 1, typ='limit')
                if bid['error'] == 0:
                    print(bid['result'])
                    __id = bid['result']['id']
                    __hash_no = bid['result']['hash']
                    __price = bid['result']['rat']
                    __total_coin = bid['result']['rec']
                    __fee = bid['result']['fee']

                    auth.create_order(trend_id=response_trend['data']['id'],
                                      orderno=__id,
                                      hashno=__hash_no,
                                      price=__price,
                                      total_coin=__total_coin,
                                      fee=__fee)

        i += 1

    auth.logout()


if __name__ == '__main__':
    main()
    sys.exit(0)
