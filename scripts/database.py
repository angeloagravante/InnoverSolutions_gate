import exceptions as ex
import os
import sqlite3

from exceptions import *

conn = sqlite3.connect("users.db")
c = conn.cursor()

def check_database():

    print (f"DEBUG: Checking database")
    #print (f"DEBUG: Database exists: {os.path.exists('users.db')}")
    try:
        if not os.path.exists("users.db"):
            c.execute("CREATE TABLE users (username TEXT PRIMARY KEY, hash_password TEXT, salt TEXT)")
            conn.commit()
        else:
            print("Database file found. Checking tables...")
            check_table()
    except Exception as e:
        raise DatabaseError(f"An error occurred while creating the database: {e}")

def check_table():
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    
    if len(users) == 0:
        raise NoUsers("No users found in the database")
    else:
        print("Users found in the database")