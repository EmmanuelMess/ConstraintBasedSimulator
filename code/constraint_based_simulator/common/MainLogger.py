import logging
from logging import Logger


def _getMainAppLogger() -> Logger:
    """
    Helper function for creating the logger used by the whole codebase. See MAIN_LOGGER.
    :return: A logger customized for this app
    """

    logger = logging.getLogger('main_app')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]\t%(message)s')  # TODO add line number and file

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    streamHandler.setFormatter(formatter)

    logger.addHandler(streamHandler)

    return logger


MAIN_LOGGER = _getMainAppLogger()
