import os
import sys
from bitkub import Bitkub
from libraries.recommendation import Recommendation, TimeInterval
from libraries.logs import Logs
from tqdm import tqdm
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
        ticker = bitkub.ticker(sym=f'THB_{sym}')
        last_price = 0
        last_percent = 0
        if len(ticker) > 0:
            data = ticker[f'THB_{sym}']
            last_price = data['last']
            last_percent = data['percentChange']

        log.print_color(f'{(i + 1)}. {sym}')
        strategy = []
        for x in timeInterval.get_interval():
            comment = recommendation.summary(symbol=sym, quote='THB', interval=x)
            summary = comment['RECOMMENDATION']
            comment = recommendation.moving_averages(symbol=sym, quote='THB', interval=x)
            mcd = comment['RECOMMENDATION']
            percent = ((i + 1) * 100) / len(result)

            # log.print_color(f'on time frame {x}')
            # log.print_color(f"SUMMARY: {summary} ==> {log.check_signal(summary)}")
            # log.print_color(f"MACD: {mcd} ==> {log.check_signal(summary)}")
            strategy.append(f'on {x} is {log.check_signal(summary)}')

        log.print_color(f'PRICE :=> {last_price} THB')
        log.print_color(f'PERCENT CHANGE :=> {last_percent}%')
        log.print_color(f"STRATEGY: {strategy}")
        log.print_color(f"PERCENT LOOP: {percent}%")
        print("\n")
        i += 1


if __name__ == '__main__':
    main()
    sys.exit(0)
