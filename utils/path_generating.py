from datetime import datetime

from data.config import log_folder


def get_log_path(date: datetime):
    date = date.strftime("%d.%m.%Y")
    return f"{log_folder}{date}.log"


def get_log_debug_path(date: datetime):
    date = date.strftime("%d.%m.%Y")
    return f"{log_folder}{date}_debug.log"
