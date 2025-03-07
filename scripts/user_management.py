import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os

def check_database():
    if not os.path.exists("users.db"):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)")
        conn.commit()
        conn.close()

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
    self.create_user_window = tk.Toplevel(parent)  # Parent is login_frame
    self.create_user_window.title("Add User")
    #self.create_user_window = tk.Toplevel()
    #self.create_user_window.title("Add User")
    #self.create_user_window.geometry("300x300")
    
    #tk.Label(self, text="Add User", font=("Arial", 18, "bold")).pack(pady=10)
    #tk.Label(self, text="Username:").pack()
    #entry_username = tk.Entry(self.create_user_window)
    #entry_username.pack(pady=5)

    #tk.Label(self.create_user_window, text="Password:").pack()
    #entry_password = tk.Entry(self.create_user_window, show="*")  # Hide password
    #entry_password.pack(pady=5)
    
    #OK = tk.Button(self.create_user_window, text="OK", command=lambda: save_user(self, entry_username.get(), entry_password.get()))
    #OK.pack(pady=10)


def save_user(self, username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("User Exists", f"User {username} already exists")
        self.create_user_window.destroy()    # Close the window after adding user
        return
    
    # close the connection
    conn.close()

    messagebox.showinfo("User Added", f"User {username} added successfully")
    self.create_user_window.destroy()    # Close the window after adding user
