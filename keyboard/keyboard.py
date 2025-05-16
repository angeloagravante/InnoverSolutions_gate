import tkinter as tk

class VirtualKeyboard(tk.Toplevel):
    def __init__(self, parent, entry):
        super().__init__(parent)
        self.title("Virtual Keyboard")
        self.configure(bg="#2C3E50")
        self.entry = entry
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.attributes("-topmost", True)  # Keep the keyboard on top
        self.create_keyboard()

    def create_keyboard(self):
        keys = [
            ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "Backspace"],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["Caps", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
            ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift"],
            ["Space"]
        ]

        for row_keys in keys:
            frame = tk.Frame(self, bg="#2C3E50")
            frame.pack(pady=2)
            for key in row_keys:
                if key == "Space":
                    button = tk.Button(frame, text="Space", width=50, height=2,
                                       bg="#3498db", fg="white", font=('Segoe UI', 10, 'bold'),
                                       command=lambda k=' ': self.key_press(k))
                else:
                    btn_width = 6 if key not in ["Tab", "Caps", "Enter", "Shift", "Backspace"] else 10
                    button = tk.Button(frame, text=key, width=btn_width, height=2,
                                       bg="#3498db", fg="white", font=('Segoe UI', 10, 'bold'),
                                       command=lambda k=key: self.key_press(k))
                button.pack(side=tk.LEFT, padx=1)

    def key_press(self, key):
        if key == "Backspace":
            current = self.entry.get()
            self.entry.delete(0, tk.END)
            self.entry.insert(0, current[:-1])
        elif key == "Enter":
            self.entry.insert(tk.END, "\n")
        elif key == "Tab":
            self.entry.insert(tk.END, "    ")
        elif key == "Caps":
            pass  # Optional caps lock logic
        elif key == "Shift":
            pass  # Optional shift logic
        else:
            self.entry.insert(tk.END, key)

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()
        self.lift()
        self.attributes("-topmost", True)  # Ensure it stays on top

# Main app window
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login with Virtual Keyboard")
        self.geometry("600x400")
        self.configure(bg="#2C3E50")

        # Create login frame
        self.login_frame = tk.Frame(self, bg="#2C3E50")
        self.login_frame.pack(pady=20)

        # Username entry
        tk.Label(self.login_frame, text="Username:", bg="#2C3E50", fg="white", font=("Segoe UI", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = tk.Entry(self.login_frame, font=("Segoe UI", 14), width=30)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password entry
        tk.Label(self.login_frame, text="Password:", bg="#2C3E50", fg="white", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(self.login_frame, font=("Segoe UI", 14), width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Create keyboard once, pass username entry by default
        self.keyboard = VirtualKeyboard(self, self.username_entry)
        self.keyboard.withdraw()

        # Bind focus to show keyboard
        self.username_entry.bind("<FocusIn>", lambda _: self.show_keyboard(self.username_entry))
        self.password_entry.bind("<FocusIn>", lambda _: self.show_keyboard(self.password_entry))

        # Add login button
        self.login_button = tk.Button(self.login_frame, text="Login", bg="#3498db", fg="white", font=("Segoe UI", 12, "bold"), command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=20)

    def show_keyboard(self, entry):
        self.keyboard.entry = entry  # Update the entry widget the keyboard interacts with
        self.keyboard.show()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Username: {username}, Password: {password}")  # Replace with actual login logic

if __name__ == "__main__":
    app = App()
    app.mainloop()