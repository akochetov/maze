import misc.settings as settings
from datetime import datetime


def log(data):
    if settings.LOG:
        print('{}\t{}'.format(datetime.now(), data))
