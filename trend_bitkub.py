import os
import sys
from termcolor import colored
from bitkub import Bitkub
from libraries.recommendation import Recommendation, TimeInterval
from libraries.auth import Authentication
from libraries.logs import Logs
from dotenv import load_dotenv

# initialize
load_dotenv()
API_KEY = os.environ.get('BITKUB_KEY')
API_SECRET = os.environ.get('BITKUB_SECRET')

bitkub = Bitkub(API_KEY, API_SECRET)
recommendation = Recommendation()
timeInterval = TimeInterval()
auth = Authentication()
log = Logs()
def main():
    auth.login()
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
        print(ticker)
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
                    scores += 1
                    text_color = 'cyan'

                print(
                    f"{colored(r['symbol'], 'cyan', attrs=['bold'])} on time {colored(x, 'blue')} is {colored(str(recomm['RECOMMENDATION']), text_color)}")

            print(f"{r['symbol']} score: {scores} percent: {ticker[str(r['bq'])]['percentChange']}%")
            print(f"-----------------------------")

            txt_trend = 'SHORT'
            if scores <= 3:
                txt_trend = 'LONG'

            auth.create_interesting(asset=r['symbol'], trend=txt_trend, price=ticker[str(r['bq'])]['last'], percent=ticker[str(r['bq'])]['percentChange'])

        i += 1

    auth.logout()


if __name__ == '__main__':
    main()
    sys.exit(0)
