import os
import sqlite3
from exceptions import DatabaseError, NoUsers
from scripts.logger import *

DB_FILE = "users.db"

def get_connection(db_file):
    """Establish a connection to the SQLite database."""
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to connect to the database: {e}")

def initialize_database():
    """Ensure the database and required tables exist."""
    if not os.path.exists(DB_FILE):
        print("Database file not found. Creating database and tables...")
        with get_connection(DB_FILE) as conn:
            c = conn.cursor()
            try:
                c.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        hash_password TEXT NOT NULL,
                        salt TEXT NOT NULL
                    )
                """)
                conn.commit()
            except sqlite3.Error as e:
                raise DatabaseError(f"An error occurred while creating the table: {e}")
    else:
        print("Database file found. Checking tables...")
        check_table()

def check_table():
    """Check if the 'users' table contains any data."""
    with get_connection(DB_FILE) as conn:
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