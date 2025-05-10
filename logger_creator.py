"""
Logger Utils

Functions that help with the creation of logging objects
"""

import logging
import os
import time
import re
import sys

argarray = sys.argv[1:]
packs = list(zip(argarray[::2], argarray[1::2]))


basepath = os.path.dirname(__file__)
os.makedirs(basepath, exist_ok=True)

log_path = os.path.join(basepath, "logs/")

error_log_filename = time.strftime("%Y%m%d_") + "error_logs.log"
all_log_filename = time.strftime("%Y%m%d_") + "all_logs.log"

log_format = "%(asctime)s | %(name)s | %(levelname)s | %(filename)s | @function %(funcName)s | line %(lineno)s | %(message)s"
date_format = "%Y-%m-%d %H:%M%S"

formatter = logging.Formatter(log_format, datefmt=date_format)
def create_handler(handler_kind: logging.Handler = logging.StreamHandler, formatter: logging.Formatter = formatter,
                   level: logging.DEBUG | logging.INFO | logging.WARNING | logging.ERROR | logging.CRITICAL = logging.DEBUG) -> logging.Handler:
    """
    Description: Create a handler

    Parameters:
    -----------
        - handler_kind (logging.Handler)

    Returns:
    --------
        - handler (logging.Handler): handler for a logger instance
    """
    if handler_kind == logging.StreamHandler:
        handler = logging.StreamHandler()
        handler.setLevel(level=level)
        handler.setFormatter(formatter)
        return handler


# with date --> new log file each day
def get_logger(log_path: str = log_path, name: str = 'Fotocasa_Logger',
               error_log_filename: str = error_log_filename, all_log_filename: str = all_log_filename,
               formatter: logging.Formatter = formatter) -> logging.Logger:
    """
    Description: Initiate logger for printing messages into log file.

    Parameters:
    -----------
        - log_path (str) : Path where the log files will be written
        - name (str) : Name of the logger

    Returns:
    --------
        - logger (logging.Logger): Logger instance that reports messages into Stream, File and Email
    """
    error_log_filepath = os.path.join(log_path, error_log_filename)
    all_log_filepath = os.path.join(log_path, all_log_filename)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Create a logger
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    # create error file handler and set level to error
    fileHandler = logging.FileHandler(filename=error_log_filepath)
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(level=logging.ERROR)

    logger.addHandler(fileHandler)

    # create debug file handler and set level to debug
    fileHandler = logging.FileHandler(filename=all_log_filepath)
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(level=logging.INFO)

    logger.addHandler(fileHandler)
    
    return logger

logger_all = get_logger(
    log_path = log_path,
    name = 'Fotocasa_Logger',
    error_log_filename =  error_log_filename,
    all_log_filename = all_log_filename,
    formatter = formatter
)
