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

    def log(self):
        f = open(f'{self.on_date}.logs.txt', 'a')
        f.write(f'run at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.close()

    def print_color(self, msg):
        n = random.randint(0, len(self.clr) - 1)
        print(colored(msg, self.clr[n]))
