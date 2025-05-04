import logging
import os
from logging.handlers import TimedRotatingFileHandler

class Logger:
    def __init__(self, log_dir="logs", log_file="activity.log", exception_log_file="exceptions.log"):
        # Ensure the log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create the full path for the log files
        log_path = os.path.join(log_dir, log_file)
        exception_log_path = os.path.join(log_dir, exception_log_file)
        
        # Configure the main logger with TimedRotatingFileHandler
        main_handler = TimedRotatingFileHandler(
            log_path, when="midnight", interval=1, backupCount=7
        )
        main_handler.setLevel(logging.INFO)
        main_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        self.logger = logging.getLogger("main_logger")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(main_handler)
        self.logger.propagate = False

        # Configure the exception logger with TimedRotatingFileHandler
        exception_handler = TimedRotatingFileHandler(
            exception_log_path, when="midnight", interval=1, backupCount=7
        )
        exception_handler.setLevel(logging.ERROR)
        exception_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        self.exception_logger = logging.getLogger("exception_logger")
        self.exception_logger.setLevel(logging.ERROR)
        self.exception_logger.addHandler(exception_handler)
        self.exception_logger.propagate = False

    def log_info(self, message):
        """Log an informational message."""
        self.logger.info(message)

    def log_warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def log_error(self, message):
        """Log an error message."""
        self.logger.error(message)
        self.exception_logger.error(message)

    def log_debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)

# Example usage
#if __name__ == "__main__":
    #logger = Logger()
    #logger.log_info("Logger initialized successfully.")
    #logger.log_warning("This is a warning message.")
    #logger.log_error("This is an error message.")
    #logger.log_debug("This is a debug message.")