import tkinter as tk
import exceptions as ex
import scripts.database as db
import threading
import serial
#import scripts.user_management as user

from scripts.database import *
from scripts.user_management import *  # Import user class
from scripts.home import home  # Import the home function
from scripts.logger import *
from scripts.arduino_module import Arduino
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

# ------------------- UI UPDATE ON BUTTON PRESS -------------------
def open_gate():
    """ Trigger gate opening event in GUI. """
    messagebox.showinfo("Gate Access", "Button Pressed! Gate Opening...")
    print("Gate Open Signal Received")

# Function to show dashboard after login
def show_dashboard():
    global dashboard_frame, content_frame  # Make dashboard_frame accessible to logout()
    
    dashboard_frame = tk.Frame(root)
    dashboard_frame.pack(fill="both", expand=True)

    # Sidebar Frame
    sidebar = tk.Frame(dashboard_frame, width=150, height=400)
    sidebar.pack(side="left", fill="y")

    # Main Content Area
    content_frame = tk.Frame(dashboard_frame, width=450, height=400)
    content_frame.pack(side="right", fill="both", expand=True)

    # Sidebar Buttons
    sections = ["Home", "Profile", "Settings"]

    for section in sections:
        btn = tk.Button(
            sidebar, 
            text=section, 
            fg="black", 
            bg="black",
            font=("Arial", 12),
            command=lambda s=section: show_content(s)  # Dynamically pass section
        )
        btn.pack(fill="x", pady=5, padx=10)        
        
        if section == "Settings":
            btn.configure(command=settings)


    # Logout Button (placed at the bottom of the sidebar)
    logout_btn = tk.Button(
        sidebar, 
        text="Logout", 
        fg="black", 
        bg="black", 
        font=("Arial", 12), 
        command=logout
    )
    logout_btn.pack(side="bottom", fill="x", pady=5, padx=10)
    # Configure sidebar to expand
    sidebar.pack_propagate(False)  # Prevent sidebar from resizing to fit content
    
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
    global dashboard_frame, content_frame  # Ensure we can access and modify the content area

    for widget in content_frame.winfo_children():
        widget.destroy()  # Clear previous content

    label = tk.Label(content_frame, text="Are you sure you want to logout?", font=("Arial", 16))
    label.pack(pady=20)

    btn_frame = tk.Frame(content_frame)
    btn_frame.pack(pady=10)

    btn_yes = tk.Button(btn_frame, text="Yes", command=lambda: confirm_logout())
    btn_yes.pack(side="left", padx=10)

    btn_no = tk.Button(btn_frame, text="No", command=lambda: show_content("Home"))
    btn_no.pack(side="left", padx=10)

def confirm_logout():
    global dashboard_frame

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

            #btn_manage_user = tk.Button(content_frame, text="Manage User", command=manage_user)
            #btn_manage_user.pack(pady=5)

def login_screen():
    login_frame = tk.Frame(root)
    login_frame.pack(fill="both", expand=True)

    tk.Label(login_frame, text="Login", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(login_frame, text="Username:").pack()
    entry_username = tk.Entry(login_frame)
    entry_username.insert(0, "admin")  # Auto-populate with "admin"
    entry_username.pack(pady=5)

    tk.Label(login_frame, text="Password:").pack()
    entry_password = tk.Entry(login_frame, show="*")  # Hide password
    entry_password.insert(0, "admin")  # Auto-populate with "admin"
    entry_password.pack(pady=5)

    def attempt_login():
        if not login(login_frame, entry_username.get(), entry_password.get()):
            tk.Label(login_frame, text="Invalid username or password", fg="red").pack()

    btn_login = tk.Button(login_frame, text="Login", command=attempt_login)
    btn_login.pack(pady=10)

# Create main window instance
root = tk.Tk()
root.title("Automatic Gate Boom Barrier System")
root.geometry("600x400")

# create Instance of logger
log = Logger()
log.log_info("Application started")

# --------- LOGIN SCREEN ---------
login_screen()

# ----------- DATABASE CHECK -----------
try:
    db.check_database()
except Exception as e:
    print("An error occurred while checking the database:", e)
    root.destroy()  # Close the window
    exit()

# Run Tkinter event loop
root.mainloop()