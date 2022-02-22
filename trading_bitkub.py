import os
import sys
from bitkub import Bitkub
from libraries.recommendation import Recommendation, TimeInterval
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

log = Logs()
def main():
    symbols = bitkub.symbols()
    result = symbols['result']
    i = 0
    while i < len(result):
        sym = str(result[i]['symbol'])[len('THB_'):]
        log.print_color(sym)
        ticker = bitkub.ticker(sym=f'THB_{sym}')
        last_price = 0
        last_percent = 0
        if len(ticker) > 0:
            data = ticker[f'THB_{sym}']
            last_price = data['last']
            last_percent = data['percentChange']

        log.print_color(f'price :=> {last_price}')
        log.print_color(f'percent :=> {last_percent}')
        recomm = recommendation.summary(symbol=sym, quote='THB', interval=timeInterval.INTERVAL_1_HOUR)
        summary = recomm['RECOMMENDATION']
        recomm = recommendation.moving_averages(symbol=sym, quote='THB', interval=timeInterval.INTERVAL_1_HOUR)
        macd = recomm['RECOMMENDATION']
        print(f"SUMMARY: {summary}")
        print(f"MACD: {macd}")

        print("\n")

        i += 1


if __name__ == '__main__':
    main()
    sys.exit(0)
