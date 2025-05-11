import logging
import os
import sqlite3

from logging.handlers import TimedRotatingFileHandler

class Logger:
    def __init__(self, log_dir="logs", log_file="activity.log", exception_log_file="exceptions.log", db_path="database_sqlite.db"):
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

        # Initialize the database
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Initialize the database and ensure the logs table exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Check if the logs table exists
            cursor.execute("""
                SELECT name FROM sqlite_master WHERE type='table' AND name='logs';
            """)
            if not cursor.fetchone():
                # Create the logs table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        message_type TEXT NOT NULL,
                        description TEXT NOT NULL,
                        full_description TEXT NOT NULL
                    )
                """)
                conn.commit()

    def log_to_database(self, level, message, full_description=""):
        """Insert a log entry into the database."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logs (timestamp, message_type, description, full_description)
                VALUES (?, ?, ?, ?)
            """, (timestamp, level, message, full_description))
            conn.commit()

    def log_info(self, message):
        """Log an informational message."""
        self.logger.info(message)
        self.log_to_database("INFO", message)

    def log_warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
        self.log_to_database("WARNING", message)

    def log_error(self, message):
        """Log an error message."""
        self.logger.error(message)
        self.exception_logger.error(message)
        self.log_to_database("ERROR", message)

    def log_debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)
        self.log_to_database("DEBUG", message)

# Example usage
#if __name__ == "__main__":
    #logger = Logger()
    #logger.log_info("Logger initialized successfully.")
    #logger.log_warning("This is a warning message.")
    #logger.log_error("This is an error message.")
    #logger.log_debug("This is a debug message.")