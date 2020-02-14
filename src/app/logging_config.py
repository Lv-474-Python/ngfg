"""
Logger to collect data (warnings,errors and critical errors) into .log file
"""
import logging
import os
from logging.handlers import RotatingFileHandler


def create_logger(log_dir):
    """
    Creates logger that saves logs to .logs file and outputs logs to console
    """
    logger = logging.getLogger('logger')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

    # Creates folder if don't exist
    os.makedirs(log_dir, exist_ok=True)
    save_filename = os.path.join(log_dir, 'warning.log')

    # Saves to file
    file_logger = RotatingFileHandler(filename=save_filename, maxBytes=1000000, backupCount=2)
    file_logger.setLevel(logging.WARNING)
    file_logger.setFormatter(formatter)
    logger.addHandler(file_logger)

    # Outputted in console
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.DEBUG)
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)

    return logger
