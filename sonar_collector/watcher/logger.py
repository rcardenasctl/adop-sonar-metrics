
import logging
import os

"""
Define the handler for info and error details about the application.
There are two handlers:
1. INFO: write the logs into a flat file with the name sonar-metrics.logs 
2. ERROR: write the logs into a flat file with the name sonar-metrics-error.logs
3. DEBUG: console stream handler to logs
"""
def init(LOGS_BASE_PATH):
    logger = logging.getLogger('sonar-logs')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages

    # Check first path does not exists
    if not os.path.exists(LOGS_BASE_PATH):
        os.makedirs(LOGS_BASE_PATH)

    LOGS_INFO_PATH = "{base_path}/sonar-metrics.logs".format(
        base_path=LOGS_BASE_PATH)
    info_handler = logging.FileHandler(LOGS_INFO_PATH)
    info_handler.setLevel(logging.INFO)

    LOGS_ERROR_PATH = "{base_path}/sonar-metrics-error.logs".format(
        base_path=LOGS_BASE_PATH)
    error_handler = logging.FileHandler(LOGS_ERROR_PATH)
    error_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
