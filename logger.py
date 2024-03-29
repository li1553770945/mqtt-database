import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    handler = TimedRotatingFileHandler(filename='app.log', when='d', interval=1, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger

