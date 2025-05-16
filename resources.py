
import os

# Base directory for resources
BASE_DIR = os.path.dirname(__file__)
# Images directory
IMAGES_DIR = os.path.join(BASE_DIR, "images")
# Example: Specific image paths
LOADING_GIF = os.path.join(IMAGES_DIR, "load.gif")
GATE_NAME_EAST = "Gate 1 East"
GATE_NAME_WEST = "Gate 1 West"

# ---------- Theme ------------
# tcl
TCL_THEME = "azure"
TCL_THEME_PATH = os.path.join(BASE_DIR, "theme", f"{TCL_THEME}.tcl")

#colorway
SECTION_BG = '#2C3E50'
MAINCONTENT_BG = "#ECF0F1"


# ---------- Keyboard Configuration ------------
# Define keyboard keys layout
KEYBOARD_LAYOUT = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

# Function to create a keyboard
def create_keyboard():
    keyboard = []
    for row in KEYBOARD_LAYOUT:
        keyboard_row = []
        for key in row:
            keyboard_row.append({"key": key, "pressed": False})
        keyboard.append(keyboard_row)
    return keyboard

# Initialize the keyboard
keyboard = create_keyboard()