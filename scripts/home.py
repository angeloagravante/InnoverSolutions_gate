import tkinter as tk
import exceptions as ex
import scripts.arduino as arduino

from arduino import *
from exceptions import *

# Create an instance of the Arduino class
arduino = Arduino(port='/dev/ttyUSB0',9600,1)

def home(parent):
    """Function to display Home section with two buttons."""
    for widget in parent.winfo_children():  # Clear previous widgets
        widget.destroy()

    tk.Label(parent, text="Welcome to Home", font=("Arial", 16)).pack(pady=10)

    def send_data_to_arduino():
        try:
            arduino.connect()
            arduino.send_data("some data")
            response = arduino.receive_data()
            print(f"Response from Arduino: {response}")
        except ex.ArduinoError as e:
            print(f"Error: {e}")

    btn1 = tk.Button(parent, text="Button 1", font=("Arial", 12), command=send_data_to_arduino)
    btn1.pack(pady=5)

    btn2 = tk.Button(parent, text="Button 2", font=("Arial", 12), command=lambda: print("Button 2 Clicked"))
    btn2.pack(pady=5)