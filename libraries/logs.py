import datetime

class Logs:
    def __init__(self):
        f = open(f'{datetime.datetime.now().strftime("%Y-%m-%d")}.logs.txt', 'a')
        f.write(f'run at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
        f.close()
