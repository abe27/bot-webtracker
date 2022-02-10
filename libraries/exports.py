import os
import json

class Exports:
    def __init__(self):
        self.__version__ = 0.1

    def export_to_json(self, filename, data):
        s = (str(filename[0:int(str(filename).find('/'))]))
        if os.path.exists(s) is False:
            os.makedirs(s)

        print(self.__version__)
        f = open(filename, 'w')
        json.dump(data, f)
        f.close()
        return True
