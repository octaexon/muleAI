from datetime import datetime
import logging
import os
import yaml

from mule import LOG_DAT, LOG_CFG

class TimestampFileHandler(logging.FileHandler):
    def __init__(self, mode='a', encoding=None, delay=False):
        filename = os.path.join(
            LOG_DAT,
            datetime.utcnow().isoformat(timespec='seconds') + '.log')
        super().__init__(filename, mode, encoding, delay)


class TimestampRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self,
                 mode='a',
                 maxBytes=0,
                 backupCount=0,
                 encoding=None,
                 delay=False):
        filename = os.path.join(
            LOG_DAT,
            datetime.utcnow().isoformat(timespec='seconds') + '.log')
        super().__init__(filename, mode, maxBytes, backupCount, encoding,
                         delay)

def load_config(cfgtag):
    filename = os.path.join(LOG_CFG, cfgtag + '.yml')
    with open(filename, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
