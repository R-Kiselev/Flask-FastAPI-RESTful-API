import logging
import os
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

format = "%(levelname)-8s %(name)s: %(message)s (%(filename)s:%(lineno)d)"
formatter = logging.Formatter(format)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(logging.INFO)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(formatter)
stderr_handler.setLevel(logging.WARNING)

log_dir = os.path.dirname(__file__)
file_handler = logging.FileHandler(f"{log_dir}.log", mode='w')
file_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)
logger.addHandler(file_handler)
