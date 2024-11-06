import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Define the minimum required Python version
required_python_version = (3, 7)

# Check if the current Python version is at least the required version
if sys.version_info < required_python_version:
    error_message = "Failure: Python version is below 3.7.\nPlease upgrade to Python 3.7 or higher."
    print(error_message)

    # Display an error dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Version Check", error_message)
    sys.exit(1)  # Exit the script

# Check for the presence of a requirements.txt file
requirements_file = "requirements.txt"

try:
    subprocess.run(["pip", "install", "-r", requirements_file], check=True)
    print("Success: Dependencies installed or upgraded.")
except subprocess.CalledProcessError as e:
    error_message = f"Failure: {str(e)}"
    print(error_message)

    # Display an error dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Version Check", error_message)
    sys.exit(1)  # Exit the script

# Check for additional packages and their versions
try:
    import numpy
    import cv2
    import PyQt5.QtCore

    # Get the absolute path to the parent directory
    parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Specify the relative path to main.py from tests folder
    program_path = os.path.join(parent_directory, "Application", "main.py")

    subprocess.run(["python", program_path])

except ImportError as e:
    error_message = f"Failure: {str(e)}"
    print(error_message)

    # Display an error dialog
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Version Check", error_message)
    sys.exit(1)  # Exit the script
