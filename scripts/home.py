import tkinter as tk
import exceptions as ex
import scripts.arduino_module as arduino_module

#from arduino_module import *
from exceptions import *

# Create an instance of the Arduino class
Arduino = arduino_module.Arduino('/dev/ttyUSB0')

# Example usage: Call the home function with a valid parent (e.g., a Tk instance)
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")  # Set window size
    home(root)
    root.mainloop()

def home(parent):
    """Function to display Home section with two buttons."""
    # Clear the parent frame
    
    for widget in parent.winfo_children():  # Clear previous widgets
        widget.destroy()

    # Ensure the parent uses grid geometry manager consistently
    parent.grid_propagate(False)

    # Add a label on the top
    tk.Label(parent, text="Welcome to Main Section", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=5)

    def button_action(row, col):
        if row == 1 and col == 1:  # Override button
            override_action()
        elif row == 1 and col == 2:  # Passing Through button
            passing_through_action()
        elif row == 1 and col == 3:  # Guest button
            guest_action()
        else:
            print(f"Button at Row {row}, Column {col} clicked")

    def override_action():
        print("Override button clicked")
        # Add your logic for the Override button here

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
            btn.grid(row=row+1, column=col, padx=10, pady=1, sticky="nsew")  # Adjust row index for label

    # Configure grid weights to make buttons expand
    for i in range(3):  # 2 rows + 1 for the label
        parent.grid_rowconfigure(i, weight=1)
    for j in range(3):  # 3 columns
        parent.grid_columnconfigure(j, weight=1)
