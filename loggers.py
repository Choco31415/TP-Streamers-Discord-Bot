"""
This is a simple config file for logging
Can be easily imported anywhere.
"""

# Handle imports
import os
import logging
from logging import handlers
import  sys

# Define variables

# Ensure logger directory exists
logger = None
log_directory = os.path.join("Resources", "Logs")

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Define logger setup
class SysLogRedirect:
    def __init__(self, level):
        self.level = level

    def write(self, message):
        if message.strip() != '':
            self.level(message)

    def flush(self):
        # create a flush method so things can be flushed when
        # the system wants to.
        self.level(sys.stderr)

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

    # Redirect standard streams
    sys.stderr = SysLogRedirect(logger.warning)

# Setup logger
setup_logger()