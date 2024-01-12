import logging
from logging import Logger


def getMainAppLogger() -> Logger:
    logger = logging.getLogger('main_app')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]\t%(message)s')

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)

    logger.addHandler(streamHandler)

    return logger


LOGGER = getMainAppLogger()
