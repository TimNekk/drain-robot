import logging
import os
from datetime import datetime

from data.config import log_folder
from utils.path_generating import get_log_path, get_log_debug_path

datefmt = '%d.%m.%Y %H:%M:%S'
format = u'%(asctime)s [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) > %(message)s'
format_debug = u'%(asctime)s [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) > %(message)s'


def get_file_handler(path: str):
    try:
        file_handler = logging.FileHandler(path, encoding='utf-8')
    except FileNotFoundError:
        os.mkdir(log_folder)
        file_handler = logging.FileHandler(path, encoding='utf-8')

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(format, datefmt))
    return file_handler


def get_file_handler_debug(path: str):
    file_handler = logging.FileHandler(path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(format_debug, datefmt))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(format, datefmt))
    return stream_handler


async def setup_logging():
    if not os.path.exists(get_log_path(datetime.now())):
        logging.root.removeHandler(logging.root.handlers[-1])
        logging.root.removeHandler(logging.root.handlers[-1])
        logging.root.addHandler(get_file_handler(get_log_path(datetime.now())))
        logging.root.addHandler(
            get_file_handler_debug(get_log_debug_path(datetime.now())))


logging.getLogger('schedule').propagate = False
logging.root.addHandler(get_stream_handler())
logging.root.setLevel(logging.DEBUG)
logging.root.addHandler(get_file_handler(get_log_path(datetime.now())))
logging.root.addHandler(
    get_file_handler_debug(get_log_debug_path(datetime.now())))
