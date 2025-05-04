import tkinter as tk
import exceptions as ex
from tkinter import messagebox  # Import messagebox for error dialogs
import scripts.database as db
import threading
import serial
import time
import queue
#import scripts.user_management as user

#from scripts.database import *
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

        return True
    else:
        for widget in login_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == "Invalid username or password":
                return False
        tk.Label(login_frame, text="Invalid username or password", fg="red").pack()
        return False

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
def check_db():
    try:
        db.get_connection(db.DB_FILE)
        db.initialize_database()
        db.check_table()
    except ex.DatabaseError as e:
        log.log_error("Database error: " + str(e))
    except ex.NoUsers as e:
        log.log_error("No users error: " + str(e))

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
        # Display loading GIF
        loading_label = tk.Label(login_frame)
        loading_label.pack(pady=10)

        try:
            from PIL import Image, ImageTk
            import os

            gif_path = os.path.join(os.path.dirname(__file__), "images", "load.gif")
            log.log_info("Loading GIF path: " + gif_path)

            gif_frames = []
            gif = Image.open(gif_path)
            for frame in range(gif.n_frames):
                gif.seek(frame)
                gif_frames.append(ImageTk.PhotoImage(gif.copy()))

            def animate(index=0):
                try:
                    loading_label.config(image=gif_frames[index])
                    root.update_idletasks()
                    root.after(50, animate, (index + 1) % len(gif_frames))  # Reduced delay to 50ms for faster playback
                except tk.TclError:
                    pass  # Ignore error if the label is destroyed

            animate()  # Start animation
        except Exception as e:
            log.log_error("Error loading GIF: " + str(e))
            loading_label.config(text="Signing in...", font=("Arial", 12))  # Fallback text if GIF is not found

        # Update the UI to show the loading GIF
        root.update_idletasks()

        def delayed_login():
            # Create a queue to communicate between threads
            result_queue = queue.Queue()

            # Perform login in a separate thread to avoid freezing the UI
            def perform_login():
                success = login(login_frame, entry_username.get(), entry_password.get())
                result_queue.put(success)  # Send result to the queue

            def check_result():
                try:
                    success = result_queue.get_nowait()  # Get result from the queue
                    loading_label.destroy()  # Remove loading GIF
                    root.update_idletasks()  # Ensure UI updates after GIF removal
                    if not success:
                        pass  # Error message is already handled in the login function
                    else:
                        show_dashboard()  # Show dashboard
                except queue.Empty:
                    root.after(100, check_result)  # Check again after 100ms if no result yet

            threading.Thread(target=perform_login).start()
            #threading.Thread(target=perform_database_check).start()
            check_result()  # Start checking for the result

        root.after(3000, delayed_login)  # Delay by 1 second (1000 ms) before starting login

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

check_db()  # Check and initialize the database


# Run Tkinter event loop
root.mainloop()