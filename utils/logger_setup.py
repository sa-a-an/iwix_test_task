import logging
import sys

def get_logger(name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    h1 = logging.StreamHandler(sys.stdout)
    h1.setFormatter(formatter)
    logger.addHandler(h1)
    return logger
