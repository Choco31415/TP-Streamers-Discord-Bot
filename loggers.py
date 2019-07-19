"""
This is a simple config file for logging
Can be easily imported anywhere.
"""

# Handle imports
import os
import logging
from logging import handlers

# Define variables

# Define other stuff
logger = None
log_directory = os.path.join("Resources", "Logs")

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

def setup_logger():
    global logger

    # Formatting
    format = "[%(asctime)s] [%(levelname)s] %(message)s"
    formatter = logging.Formatter(format, datefmt='%m/%d %I:%M:%S %p')

    # Set handlers
    handler = logging.handlers.RotatingFileHandler(os.path.join(log_directory, "Log.txt"), 'a', 20000, 4)
    handler.setFormatter(formatter)

    # Update logger
    logger = logging.getLogger("File Logger")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.propagate = False # Avoid console output

setup_logger()