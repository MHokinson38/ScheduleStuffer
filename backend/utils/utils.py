##############################
# General utility functions for whole backend 
#
# Matt Hokinson, 12/26/22
##############################

import enum

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

def log(message, mode=LoggingMode.DEBUG):
    """Log a message to the console, with a mode to determine what to log

    Args:
        message (string): Message to log
        mode (LoggingMode, optional): Logging mode. Defaults to LoggingMode.DEBUG.
    """
    if mode == LoggingMode.DEBUG and DEBUG_LOG_ON:
        print("[DEBUG] " + message)
    elif mode == LoggingMode.INFO and INFO_LOG_ON:
        print("[INFO] " + message)
    elif mode == LoggingMode.WARNING and WARNING_LOG_ON:
        print("[WARNING] " + message)
    elif mode == LoggingMode.ERROR and ERROR_LOG_ON:
        print("[ERROR] " + message)