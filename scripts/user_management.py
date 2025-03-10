import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import hashlib

def user_management_frame(parent):
    frame = ttk.Frame(parent)
    ttk.Label(frame, text="User Management Section").pack(pady=20)
    
    # Example: Add a user list
    user_list = tk.Listbox(frame)
    user_list.pack(pady=0, padx=10, fill="both", expand=True)
    
    # Example: Add dummy users
    users = ["Alice", "B1ob", "Charlie"]
    for user in users:
        user_list.insert(tk.END, user)
    
    return frame


def add_user(self, parent):
    #self.create_user_window = tk.Toplevel(parent)  # Parent is login_frame
    #self.create_user_window.title("Add User")
    self.create_user_window = tk.Toplevel()
    self.create_user_window.title("Add User")
    self.create_user_window.geometry("300x300")
    
    tk.Label(self, text="Add User", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(self, text="Username:").pack()
    entry_username = tk.Entry(self.create_user_window)
    entry_username.pack(pady=5)

    tk.Label(self.create_user_window, text="Password:").pack()
    entry_password = tk.Entry(self.create_user_window, show="*")  # Hide password
    entry_password.pack(pady=5)

    OK = tk.Button(self.create_user_window, text="OK", command=lambda: user(entry_username.get(), entry_password.get()).insert_user())
    OK.pack(pady=10)

class user:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password
        
    # Function to salt and hash a password
    def hash_password(self, password):
        salt = os.urandom(16)
        salted_password = password.encode('utf-8') + salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()
    
        return salt.hex(), hashed_password

    def insert_user(self ):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        try:

            #print(f"DEBUG: Username = {self.username}, Password = {self.password}")  # Debugging line

            salt, hashed_password = user.hash_password(self, self.password)
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (self.username,hashed_password, salt ))
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("User Exists", f"User {self.username} already exists")
            return
        
        # close the connection
        conn.close()

        messagebox.showinfo("User Added", f"User {self.username} added successfully")

    def delete_user(self):
        self.delete_user_window = tk.Toplevel()
        self.delete_user_window.title("Delete User")
        self.delete_user_window.geometry("300x300") # Set window size 
    
    #return true or false if user exists    
    def authenticate(self):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        
        c.execute("SELECT hash_password, salt FROM users WHERE username=?", (self.username,))
        user = c.fetchone()
        conn.close()

        if user:
            stored_hash_password, stored_salt = user
            salted_password = self.password.encode('utf-8') + bytes.fromhex(stored_salt)
            hashed_password = hashlib.sha256(salted_password).hexdigest()
            if hashed_password == stored_hash_password:
                    return True
        return False
