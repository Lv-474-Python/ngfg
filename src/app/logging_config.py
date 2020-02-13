"""
Logger to collect data (warnings,errors and critical errors) into .logs file
"""
import logging


def create_logger():
    """
    Creates logger that saves logs to .logs file and outputs logs to console
    """
    logger = logging.getLogger('file_console_logger')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

    # Saves to file
    # TODO add creaton of log folder
    file_logger = logging.FileHandler(filename='WARNINGS.logs')
    file_logger.setLevel(logging.WARNING)
    file_logger.setFormatter(formatter)
    logger.addHandler(file_logger)

    # Outputted in console
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.DEBUG)
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)

    return logger
