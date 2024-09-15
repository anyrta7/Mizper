# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2024 Anyrta7
#
# You are free to use, modify, and distribute this software under the MPL 2.0 license, with the requirement
# to disclose any modifications to this file. Other files in the project may remain under different licenses.
import logging
import shutil
import sys
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define colorama colors
INFO_COLOR = Fore.GREEN
ERROR_COLOR = Fore.RED
WARN_COLOR = Fore.YELLOW
SUCCESS_COLOR = Fore.LIGHTGREEN_EX
LIGHT = Fore.LIGHTWHITE_EX

# Configure logger
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_file = 'mizper.log'
log_max_size = 10000000  # 10 MB

file_handler = RotatingFileHandler(log_file, maxBytes=log_max_size, backupCount=5)
file_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler])


def print_banner():
    executeable = sys.argv[0]
    binary = False
    if executeable.endswith('.py') and hasattr(sys, 'frozen'):
        binary = True
    BANNER = r"""
 __   __  ___   _______  _______  _______  ______   
|  |_|  ||   | |       ||       ||       ||    _ |  
|       ||   | |____   ||    _  ||    ___||   | ||  
|       ||   |  ____|  ||   |_| ||   |___ |   |_||_ 
|       ||   | | ______||    ___||    ___||    __  |
| ||_|| ||   | | |_____ |   |    |   |___ |   |  | |
|_|   |_||___| |_______||___|    |_______||___|  |_|
"""
    print(Fore.LIGHTRED_EX + BANNER + Style.RESET_ALL + ("Executable version\n" if binary else ''))


def log_info(message):
    """Log an info message with colorama."""
    message_print = f"[{INFO_COLOR}INF{Style.RESET_ALL}] {message}"
    logging.info(message)
    print(message_print)


def log_warn(message):
    """Log an info message with colorama."""
    message_print = f"[{WARN_COLOR}WRN{Style.RESET_ALL}] {message}"
    logging.warning(message)
    print(message_print)


def log_error(message):
    """Log an error message with colorama."""
    message_print = f"[{ERROR_COLOR}ERR{Style.RESET_ALL}] {message}"
    logging.error(message)
    print(message_print)


def log_sucs(message):
    """  """
    message_print = f"[{SUCCESS_COLOR}SUC{Style.RESET_ALL}] {LIGHT}{message}{Style.RESET_ALL}"
    print(message_print)


def inp(message):
    message_print = f"[{WARN_COLOR}INP{Style.RESET_ALL}] {message}"
    text = input(message_print)
    return text


def truncate_text(text):
    width = shutil.get_terminal_size().columns
    if len(text) > width:
        return text[:width - 15] + '...'
    return text
