import logging
from traceback import format_exception


def get_logger():
    logger = logging.getLogger(__package__)
    handler = logging.FileHandler(__package__ + '.log')
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def except_hooking(exc_type, exc_value, traceback):
    logger = get_logger()
    logger.critical(format_exception(exc_type, exc_value, traceback))
