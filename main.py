import tkinter as tk
from scripts.user_management import user  # Import the login function
from scripts.user_management import *  # Import the home function
from scripts.home import home  # Import the home function

# Function to verify login
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if user(username, password):  # Call function from login.py
        login_frame.pack_forget()  # Hide login screen
        show_dashboard()  # Show dashboard

# Function to show dashboard after login
def show_dashboard():
    dashboard_frame.pack(fill="both", expand=True)

# Function to update content area
def show_content(section):
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    label = tk.Label(content_frame, text=f"Welcome to {section}", font=("Arial", 16), bg="white")
    label.pack(pady=50)

# Create main window
root = tk.Tk()
root.title("Automatic Gate Boom Barrier System")
root.geometry("600x400")

# ----------- DATABASE CHECK -----------
try:
    check_database()
except Exception as e:
    print("An error occurred while checking the database:", e)
    root.destroy()  # Close the window
    exit()

# --------- LOGIN SCREEN ---------
login_frame = tk.Frame(root)
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="Login", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(login_frame, text="Username:").pack()
entry_username = tk.Entry(login_frame)
entry_username.pack(pady=5)

tk.Label(login_frame, text="Password:").pack()
entry_password = tk.Entry(login_frame, show="*")  # Hide password
entry_password.pack(pady=5)

btn_login = tk.Button(login_frame, text="Login", command=login)
btn_login.pack(pady=10)

# create a TK hyperlink to add a user
#btn_add_user = tk.Button(login_frame, text="Add User", command=add_user)
btn_add_user = tk.Button(login_frame, text="Add User", command=lambda: add_user(login_frame, root))
btn_add_user.pack(pady=10)


# --------- DASHBOARD SCREEN (Hidden initially) ---------
dashboard_frame = tk.Frame(root)

# Sidebar Frame
sidebar = tk.Frame(dashboard_frame, bg="#2C3E50", width=150, height=400)
sidebar.pack(side="left", fill="y")

# Sidebar Buttons
sections = ["Home", "Profile", "Settings", "Logout"]

for section in sections:
    btn = tk.Button(
        sidebar, 
        text=section, 
        fg="white", 
        bg="#34495E",
        font=("Arial", 12),
        command=(home if section == "Home" else lambda s=section: show_content(s))  # Pass section name dynamically
    )
    btn.pack(fill="x", pady=5, padx=10)

# Main Content Area
content_frame = tk.Frame(dashboard_frame, bg="white", width=450, height=400)
content_frame.pack(side="right", fill="both", expand=True)

# Default content
show_content("Home")

# Run Tkinter event loop
root.mainloop()