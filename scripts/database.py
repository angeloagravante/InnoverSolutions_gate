import os
import sqlite3
from exceptions_class import DatabaseError, NoUsers
from scripts.logger import *

class DatabaseManager:
    DB_FILE = "database_sqlite.db"

    def __init__(self, db_file=None):
        self.db_file = db_file or self.DB_FILE

    # ----------------- Properties -----------------
    @property
    def db_file(self):
        return self._db_file
    @db_file.setter
    def db_file(self, value):
        if not isinstance(value, str):
            raise ValueError("Database file path must be a string.")
        if not value.endswith('.db'):
            raise ValueError("Database file must have a .db extension.")
        self._db_file = value

    @property
    def isConnected(self):
        """Check if the database connection is established."""
        try:
            conn = self.get_connection()
            conn.close()
            return True
        except sqlite3.Error:
            return False
    # ----------------- Methods -----------------

    def get_connection(self):
        """Establish a connection to the SQLite database."""
        try:
            return sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            raise DatabaseError(f"Failed to connect to the database: {e}")

    # def initialize_database(self):
    #     """Ensure the database and required tables exist."""
    #     if not os.path.exists(self.db_file):
    #         print("Database file not found. Creating database...")
    #     try:
    #         open(self.db_file, 'w').close()  # Create an empty database file
    #         print("Database file created. Initializing tables...")
    #     except sqlite3.Error as e:
    #         raise DatabaseError(f"An error occurred while creating the tables: {e}")
        
    def check_table(self):
        """Check if the 'users' table contains any data."""
        with self.get_connection() as conn:
            c = conn.cursor()
            try:
                c.execute("SELECT COUNT(*) FROM users")
                user_count = c.fetchone()[0]
                if user_count == 0:
                    raise NoUsers("No users found in the database")
                else:
                    print(f"Users found in the database: {user_count}")
            except sqlite3.Error as e:
                raise DatabaseError(f"An error occurred while checking the table: {e}")
    
    def insert_log(self, log_type, log_description, full_description=None):
        """Insert a log entry into the 'logs' table."""
        with self.get_connection() as conn:
            c = conn.cursor()
            try:
                c.execute("""
                    INSERT INTO logs (timestamp, log_type, log_description, full_description)
                    VALUES (datetime('now'), ?, ?, ?)
                """, (log_type, log_description, full_description))
                conn.commit()
            except sqlite3.Error as e:
                raise DatabaseError(f"An error occurred while inserting the log: {e}")
    def get_logs(self):
        """Retrieve all log entries from the 'logs' table."""
        with self.get_connection() as conn:
            c = conn.cursor()
            try:
                c.execute("SELECT * FROM logs")
                logs = c.fetchall()
                return logs
            except sqlite3.Error as e:
                raise DatabaseError(f"An error occurred while retrieving the logs: {e}")
    def clear_logs(self):
        """Clear all log entries from the 'logs' table."""
        with self.get_connection() as conn:
            c = conn.cursor()
            try:
                c.execute("DELETE FROM logs")
                conn.commit()
            except sqlite3.Error as e:
                raise DatabaseError(f"An error occurred while clearing the logs: {e}")
    def close_connection(self, conn):
        """Close the database connection."""
        if conn:
            conn.close()
            print("Database connection closed.")
        else:
            print("No connection to close.")
    def __del__(self):
        """Destructor to ensure the database connection is closed."""
        try:
            self.close_connection(self.get_connection())
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")
    
    def user_exists(self, rfid):
        """Check if a user exists in the database."""
        with self.get_connection() as conn:
            c = conn.cursor()
            try:
                c.execute("SELECT rfid FROM users WHERE rfid = ?", (rfid,))
                user = c.fetchone()
                return user is not None
            except sqlite3.Error as e:
                raise DatabaseError(f"An error occurred while checking if the user exists: {e}")