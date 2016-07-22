import logging
from traceback import format_exception

_logger_filename = __package__ + '.log'
_logger = logging.getLogger(__package__)
_handler = logging.FileHandler(_logger_filename)
_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
_handler.setFormatter(_formatter)
_logger.addHandler(_handler)
_logger.setLevel(logging.INFO)


def get_logger():
    return _logger


def except_hooking(exc_type, exc_value, traceback):
    logger = get_logger()
    logger.critical(format_exception(exc_type, exc_value, traceback))
