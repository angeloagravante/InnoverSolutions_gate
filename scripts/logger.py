import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs", log_file="activity.log", exception_log_file="exceptions.log"):
        # Ensure the log directory exists
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create the full path for the log files
        log_path = os.path.join(log_dir, log_file)
        exception_log_path = os.path.join(log_dir, exception_log_file)
        
        # Configure the main logger
        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger()

        # Configure the exception logger
        self.exception_logger = logging.getLogger("exception_logger")
        exception_handler = logging.FileHandler(exception_log_path)
        exception_handler.setLevel(logging.ERROR)
        exception_handler.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
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