import datetime

class Logs:
    def __init__(self):
        f = open(f'{datetime.datetime.now().strftime("%Y-%m-%d")}.logs.txt', 'w')
        f.write(f'run at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\r')
        f.close()