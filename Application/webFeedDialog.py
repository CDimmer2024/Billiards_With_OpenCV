from PyQt5.QtWidgets import QPushButton, QDialog, QHBoxLayout, QVBoxLayout, QLineEdit, \
    QLabel, QFrame, QMessageBox
from PyQt5.QtCore import Qt


class MyDialog(QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        # Calculate 50% of the parent (main window) dimensions
        parent_geometry = parent.geometry()
        dialog_width = parent_geometry.width() // 2
        dialog_height = parent_geometry.height() // 10

        self.setWindowTitle("Input Dialog")
        self.setFixedSize(dialog_width, dialog_height)  # Set size to 50% of the main window's dimensions
        self.setWindowFlag(Qt.FramelessWindowHint)  # Create a frameless window

        # Create a frame to simulate a border
        border_frame = QFrame(self)
        border_frame.setFrameShape(QFrame.StyledPanel)
        border_frame.setFrameShadow(QFrame.Sunken)
        border_frame.setGeometry(0, 0, dialog_width, dialog_height)  # Adjust the geometry to match the dialog's size

        # Create a QLabel for the prompt
        prompt_label = QLabel("Enter Web Address:", self)
        prompt_label.setAlignment(Qt.AlignCenter)  # Center the text

        # Create a text entry field
        self.text_entry = QLineEdit(self)
        self.text_entry.setPlaceholderText("Web Address here...")
        self.text_entry.setFocus()  # Set the focus on the entry field

        # Create "Submit" and "Cancel" buttons
        submit_button = QPushButton("Submit", self)
        submit_button.clicked.connect(self.submit_clicked)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.close)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        button_layout.addWidget(cancel_button)

        # Create a vertical layout for the dialog
        layout = QVBoxLayout(self)
        layout.addWidget(prompt_label)
        layout.addWidget(self.text_entry)
        layout.addLayout(button_layout)

    def submit_clicked(self):
        # Get the text from the entry field
        entered_text = self.text_entry.text()

        # Check if the entered text starts with "http"
        if entered_text.startswith("http"):
            self.accept()
            self.parent().setVideoFeed(entered_text)
        else:
            # Show an error message
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid web address starting with 'http'.")
