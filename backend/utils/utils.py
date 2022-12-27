##############################
# General utility functions for whole backend 
#
# Matt Hokinson, 12/26/22
##############################

import enum
import datetime

# Create enum for different logging modes 
class LoggingMode(enum.Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 3

# All on by default, config with CLA maybe (TODO) 
DEBUG_LOG_ON = True 
INFO_LOG_ON = True 
WARNING_LOG_ON = True 
ERROR_LOG_ON = True 

# Logging file 
LOGGING_FILE = "utils/logs/server_log.log"

def log(message, mode=LoggingMode.DEBUG):
    """Log a message to the console, with a mode to determine what to log

    Args:
        message (string): Message to log
        mode (LoggingMode, optional): Logging mode. Defaults to LoggingMode.DEBUG.
    """
    log_message = ""
    timestamp = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    if mode == LoggingMode.DEBUG and DEBUG_LOG_ON:
        log_message = f"[{timestamp}][DEBUG] " + message
    elif mode == LoggingMode.INFO and INFO_LOG_ON:
        log_message = f"[{timestamp}][INFO] " + message
    elif mode == LoggingMode.WARNING and WARNING_LOG_ON:
        log_message = f"[{timestamp}][WARNING] " + message
    elif mode == LoggingMode.ERROR and ERROR_LOG_ON:
        log_message = f"[{timestamp}][ERROR] " + message

    # print the log message nad append to log file 
    print(log_message)
    with open(LOGGING_FILE, 'a') as f:
        f.write(log_message + "\n")
