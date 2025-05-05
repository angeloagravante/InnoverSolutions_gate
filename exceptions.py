from scripts.logger import *  # Import the existing logger


logger = Logger()

class AppError(Exception):
    """Base class for application-specific errors."""
    def __init__(self, message="An application error occurred"):
        super().__init__(message)
        logger.log_error(message)

class DatabaseError(AppError):
    """Exception for database-related errors."""
    def __init__(self, message="Database connection failed"):
        super().__init__(message)

class ValidationError(AppError):
    """Exception for invalid inputs."""
    def __init__(self, message="Invalid input provided"):
        super().__init__(message)

class NoUsers(AppError):
    """Exception for no users found in the database."""
    def __init__(self, message="No users found in the database"):
        super().__init__(message)

class ArduinoError(Exception):
    """Base class for Arduino"""
    def __init__(self, message="Arduino connection failed"):
        super().__init__(message)
        logger.log_error(message)

class SerialError(ArduinoError):
    """Exception for serial port errors."""
    def __init__(self, message="Serial port connection failed"):
        super().__init__(message)

class SerialTimeoutError(SerialError):
    """Exception for serial port timeout errors."""
    def __init__(self, message="Serial port connection timed out"):
        super().__init__(message)

class SerialDataError(SerialError):
    """Exception for serial port data errors."""
    def __init__(self, message="Invalid data received from serial port"):
        super().__init__(message)

class SerialPermissionError(SerialError):
    """Exception for serial port permission errors."""
    def __init__(self, message="Permission denied for serial port"):
        super().__init__(message)
