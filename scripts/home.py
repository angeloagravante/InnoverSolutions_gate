import tkinter as tk
import scripts.arduino_module as arduino_module
import scripts.logger as logger
import threading
import resources

#from arduino_module import *
from exceptions_class import *
from scripts.database import *
from resources import *

log = Logger()  # Create an instance of the Logger
db = DatabaseManager()  # Create an instance of the DatabaseManager
# Connect to the Arduino
import serial.tools.list_ports

def detect_arduino_port():
    """Automatically detect the Arduino port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Check for common Arduino identifiers in the port description
        if "IOUSBHostDevice" in port.description or "tty" in port.device or "Arduino" in port.description:
            print(f"Arduino detected on port: {port.device}")
            log.log_info(f"Arduino detected on port: {port.device}")
            return port.device
    return None

def connect_to_arduino():
    """Attempt to connect to the Arduino."""
    try:
        detected_port = detect_arduino_port()
        if detected_port:
            global Arduino
            Arduino = arduino_module.Arduino(port=detected_port, baud_rate=9600)
            Arduino.connect()
            # Check if the connection was successful
            if Arduino.is_connected:
                log.log_info(f"Connected to Arduino on port {Arduino.port}")
                return True
        else:
            print("No Arduino device detected.")
            log.log_error("No Arduino device detected.")
            return False
    except ArduinoError as e:
        print(f"SerialException: Failed to connect to Arduino: {e}")
        log.log_error(f"Failed to connect to Arduino: {e}")
        return False

# Initial attempt to connect to Arduino
Arduino = None
connect_to_arduino()

def home(parent):
    """Function to display Home section with two buttons."""
    try:
        if Arduino.is_connected:
            Arduino.reset()  # Reset the Arduino connection
        else:
            if not connect_to_arduino():
                print("Failed to connect to Arduino.")
                log.log_error("Failed to connect to Arduino.")
    except Exception as e:
        log.log_error("Error resetting Arduino connection: " + str(e))
    # Clear the parent frame
    for widget in parent.winfo_children():  # Clear previous widgets
        widget.destroy()

    # Ensure the parent uses grid geometry manager consistently
    parent.grid_propagate(False)

    # Add a label on the top
    tk.Label(parent, text="Welcome to Main Section", font=("Arial", 16),bg=MAINCONTENT_BG).grid(row=0, column=0, columnspan=3, pady=5)

    def button_action(row, col):
        if row == 1 and col == 1:  # Override button
            override_action()
        elif row == 1 and col == 2:  # Passing Through button
            passing_through_action()
        elif row == 1 and col == 3:  # Guest button
            guest_action()
        else:
            print(f"Button at Row {row}, Column {col} clicked")
            
    def no_rfid_connected_screen():
        for widget in parent.winfo_children():
            widget.destroy()

        # Add override content to the main content area
        tk.Label(parent, text="No RFID reader connected", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=20)
        tk.Button(parent, text="Back", command=lambda: home(parent)).grid(row=2, column=1, columnspan=1, pady=10)

    def override_action():
        print("Override button clicked")

        try:
            if Arduino.is_connected:
                Arduino.reset()  # Reset the Arduino connection
            else:
                if not connect_to_arduino():
                    print("Failed to connect to Arduino.")
        except Exception as e:
            no_rfid_connected_screen()
            return

        # Clear the parent frame and display entrance and exit buttons
        for widget in parent.winfo_children():
            widget.destroy()
            tk.Label(parent, text="Select Gate to Override", font=("Arial", 16),bg=MAINCONTENT_BG).grid(row=0, column=0, columnspan=2, pady=5)

            # Create a frame to center the buttons
            button_frame = tk.Frame(parent)
            button_frame.grid(row=1, column=0, columnspan=2, pady=20)

            for row in range(1):
                for col in range(2):
                    labels = [["Entrance", "Exit"]]

                    # Create 2 buttons for exit and entrance with larger size
                    btn = tk.Button(
                        button_frame,
                        text=labels[row][col],
                        font=("Arial", 14, "bold"),  # Increase font size
                        bg=MAINCONTENT_BG,
                        fg="black",  # Change text color for better visibility
                        width=15,  # Set button width
                        height=10,  # Set button height
                        command=lambda r=row, c=col: show_rfid_screen(r+1, c+1)
                    )
                    btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Configure grid weights to make buttons expand equally within the frame
            for i in range(2):  # 1 row
                button_frame.grid_rowconfigure(i, weight=1)
            for j in range(2):  # 2 columns
                button_frame.grid_columnconfigure(j, weight=1)

        # Configure parent grid to center the button frame
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        def show_rfid_screen(row,col):
            if row == 1 and col == 1:
                rfid_screen()
            elif row == 1 and col == 2:
                rfid_screen()

        def rfid_screen():
            for widget in parent.winfo_children():
                widget.destroy()
            try:
                Arduino.reset()
            except Exception as e:
                no_rfid_connected_screen()
                log.log_error("Error resetting Arduino connection: " + str(e))
                return

            # Add override content to the main content area
            tk.Label(parent, text="Scan your RFID", font=("Arial", 14)).grid(row=0, column=0, columnspan=3, pady=20)
            # Add an RFID image
            rfid_image = tk.PhotoImage(file="images/wifi.png")  # Replace with the actual path to your RFID image
            resized_image = rfid_image.subsample(2, 2)  # Adjust the subsample values to resize the image
            rfid_label = tk.Label(parent, image=resized_image)
            rfid_label.image = resized_image  # Keep a reference to avoid garbage collection
            rfid_label.grid(row=1, column=0, columnspan=3, pady=10)
            # tk.Button(parent, text="Back", command=lambda: home(parent)).grid(row=2, column=1, columnspan=1, pady=10)

            # Use a separate thread to read RFID data from the Arduino
            def read_rfid():
                if Arduino:
                    try:
                        # Read RFID data from the Arduino
                        rfid_data = Arduino.read_rfid()
                        if rfid_data:
                            print(f"RFID: {rfid_data}")
                            # Process the scanned RFID data here
                            if rfid_data:
                                    if db.user_exists(rfid_data):
                                        Arduino.send_data(Arduino.OPEN_GATE)  # Send a response to Arduino
                                        Message = f"User {rfid_data} authorized."
                                        Arduino.reset()  # Reset the Arduino connection
                                    else:
                                        print("User not found in the database.")
                                        Message = f"User {rfid_data} unauthorized."

                        elif not rfid_data:
                            Message = "RFID scan failed. Please try again."
                            
                        # Display the message on the screen
                        tk.Label(parent, text=Message, font=("Arial", 12)).grid(row=3, column=0, columnspan=3, pady=10)
                        parent.after(2000, lambda: home(parent))  # Return to home after 2 seconds
                    except SerialTimeoutError as e:
                        print(f"Timeout error while reading RFID: {e}")
                    except Exception as e:
                        print(f"Error reading RFID: {e}")
                else:
                    print("Arduino is not connected. Cannot read RFID.")

            threading.Thread(target=read_rfid, daemon=True).start()

    def passing_through_action():
        print("Passing Through button clicked")
        # Add your logic for the Passing Through button here

    def guest_action():
        print("Guest button clicked")
        # Add your logic for the Guest button here

    # Create a 2x3 grid of buttons
    for row in range(1):
        for col in range(3):
            labels = [
                ["Override", "Passing Through", "Guest"],
                #["Hidden Button", "Hidden Button", "Hidden Button"]
            ]
            is_hidden = labels[row][col] == "Hidden Button"
            btn = tk.Button(
                parent,
                text=labels[row][col] if not is_hidden else " ",
                font=("Arial", 12, "bold"),
                bg="black",
                fg="black",
                #highlightbackground="black",
                #highlightthickness=0.05,
                wraplength=50 if labels[row][col] == "Passing Through" else 0,  # Wrap text if label is "Passing Through"
                state="disabled" if is_hidden else "normal",
                command=lambda r=row, c=col, hidden=is_hidden: button_action(r+1, c+1) if not hidden else None
            )
            btn.grid(row=row+1, column=col, padx=5, pady=1, sticky="nsew")  # Adjust row index for label

    # Configure grid weights to make buttons expand
    for i in range(3):  # 2 rows + 1 for the label
        parent.grid_rowconfigure(i, weight=1)
    for j in range(3):  # 3 columns
        parent.grid_columnconfigure(j, weight=1)

# Example usage: Call the home function with a valid parent (e.g., a Tk instance)
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  # Set window size
    home(root)
    root.mainloop()