import datetime
import random
from termcolor import colored


class Logs:
    def __init__(self):
        self.on_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.clr = [
            'grey',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
        ]
        self.sign = ['🔺', '🔺🔺', '🔻', '🔻🔻', '–'];

    def log(self):
        f = open(f'{self.on_date}.logs.txt', 'a')
        f.write(f'run at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.close()

    def print_color(self, msg):
        n = random.randint(0, len(self.clr) - 1)
        print(colored(msg, self.clr[n]))

    def check_signal(self, sign):
        if sign == 'STRONG_SELL':
            return self.sign[3]

        elif sign == 'SELL':
            return self.sign[2]

        elif sign == 'BUY':
            return  self.sign[0]

        elif sign == 'STRONG_BUY':
            return self.sign[1]

        return self.sign[4]
