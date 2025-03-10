import tkinter as tk
import exceptions as ex
import scripts.database as db
#import scripts.user_management as user

from scripts.database import *
from scripts.user_management import *  # Import user class
from scripts.home import home  # Import the home function
from exceptions import *

# Function to verify login
def login(login_frame, username, password):
    User = user(username, password)
    
    if User.authenticate():  # Call function from login.py
        login_frame.pack_forget()  # Hide login screen
        show_dashboard()  # Show dashboard
    else:
        for widget in login_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == "Invalid username or password":
                return 
        tk.Label(login_frame, text="Invalid username or password", fg="red").pack()

# Function to show dashboard after login
def show_dashboard():
    global dashboard_frame, content_frame  # Make dashboard_frame accessible to logout()
    
    dashboard_frame = tk.Frame(root)
    dashboard_frame.pack(fill="both", expand=True)

    # Sidebar Frame
    sidebar = tk.Frame(dashboard_frame, bg="#2C3E50", width=150, height=400)
    sidebar.pack(side="left", fill="y")

    # Main Content Area
    content_frame = tk.Frame(dashboard_frame, bg="white", width=450, height=400)
    content_frame.pack(side="right", fill="both", expand=True)

    # Sidebar Buttons
    sections = ["Home", "Profile", "Settings", "Logout"]

    for section in sections:
        btn = tk.Button(
            sidebar, 
            text=section, 
            #fg="white", 
            bg="#34495E",
            font=("Arial", 12),
            command=lambda s=section: show_content(s)  # Dynamically pass section
        )
        btn.pack(fill="x", pady=5, padx=10)

        if section == "Logout":
            btn.configure(command=logout)   
        
        if section == "Settings":
            btn.configure(command=settings)

    # Default content
    show_content("Home")  # Ensure home section loads first

# Function to update content area
def show_content(section):
    for widget in content_frame.winfo_children():
        widget.destroy()  # Clear previous content

    if section == "Home":
        home(content_frame)  # Pass content_frame as parent to home function
    else:
        label = tk.Label(content_frame, text=f"Welcome to {section}", font=("Arial", 16), bg="white")
        label.pack(pady=50)

# Function to logout
def logout():
    global dashboard_frame  # Ensure we can access and destroy it

    if dashboard_frame:
        dashboard_frame.destroy()  # Remove the dashboard

    login_screen()  # Show the login screen again
    root.update_idletasks()  # Force UI update

# Function to display settings
def settings():
    for widget in content_frame.winfo_children():
        widget.destroy()  # Clear previous content

    label = tk.Label(content_frame, text="Settings", font=("Arial", 16), bg="white")
    label.pack(pady=10)

    # Create sections/categories
    categories = ["User Management"]

    for category in categories:
        category_label = tk.Label(content_frame, text=category, font=("Arial", 14, "bold"), bg="white")
        category_label.pack(pady=5)

        if category == "User Management":
            btn_add_user = tk.Button(content_frame, text="Add User", command=lambda: add_user(content_frame))
            btn_add_user.pack(pady=5)

            btn_manage_user = tk.Button(content_frame, text="Manage User", command=manage_user)
            btn_manage_user.pack(pady=5)

def login_screen():
    login_frame = tk.Frame(root)
    login_frame.pack(fill="both", expand=True)

    tk.Label(login_frame, text="Login", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(login_frame, text="Username:").pack()
    entry_username = tk.Entry(login_frame)
    entry_username.pack(pady=5)

    tk.Label(login_frame, text="Password:").pack()
    entry_password = tk.Entry(login_frame, show="*")  # Hide password
    entry_password.pack(pady=5)

    btn_login = tk.Button(login_frame, text="Login", command=lambda: login(login_frame, entry_username.get(), entry_password.get()))
    btn_login.pack(pady=10)

# Create main window instance
root = tk.Tk()
root.title("Automatic Gate Boom Barrier System")
root.geometry("600x400")

# ----------- DATABASE CHECK -----------
try:
    db.check_database()
except Exception as e:
    print("An error occurred while checking the database:", e)
    root.destroy()  # Close the window
    exit()

# --------- LOGIN SCREEN ---------
login_screen()

# Run Tkinter event loop
root.mainloop()