class AppError(Exception):
    """Base class for application-specific errors."""
    pass

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

# Using the custom exceptions
#try:
#    raise DatabaseError()  # Raises a database error
#except AppError as e:  # Catching all custom exceptions
#    print(f"Application Error: {e}")

#try:
#    raise ValidationError("Username is required")  # Raises validation error
#except ValidationError as e:
#    print(f"Validation Failed: {e}")

#try:
#    raise NoUsers()  # Raises no users error
#except NoUsers as e:
#    print(f"No Users Found: {e}")
# Output
# Application Error: Database connection failed  
# Validation Failed: Username is required