import tkinter as tk
import exceptions as ex

from exceptions import *

def home(parent):
    """Function to display Home section with two buttons."""
    for widget in parent.winfo_children():  # Clear previous widgets
        widget.destroy()

    tk.Label(parent, text="Welcome to Home", font=("Arial", 16)).pack(pady=10)

    btn1 = tk.Button(parent, text="Button 1", font=("Arial", 12), command=lambda: print("Button 1 Clicked"))
    btn1.pack(pady=5)

    btn2 = tk.Button(parent, text="Button 2", font=("Arial", 12), command=lambda: print("Button 2 Clicked"))
    btn2.pack(pady=5)