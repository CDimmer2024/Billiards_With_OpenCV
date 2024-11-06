from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, QDesktopWidget

class TeamNameDialog(QDialog):
    def __init__(self, parent=None):
        super(TeamNameDialog, self).__init__(parent)

        # Set title of window
        self.setWindowTitle("Enter Team Name(s)")

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        # Set the position and size of the window
        self.setGeometry(0, 0, 400, 200)

        # Set window to center of user's screen
        self.centerOnScreen()

        # Team 1 label and input
        self.team1_label = QLabel("Team 1:")
        self.team1_edit = QLineEdit(self)

        # Team 2 label and input
        self.team2_label = QLabel("Team 2:")
        self.team2_edit = QLineEdit(self)

        # Button box with OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)

        # Connect the accepted and rejected signals to corresponding slots
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Vertical layout to arrange the widgets vertically
        layout = QVBoxLayout(self)
        layout.addWidget(self.team1_label)
        layout.addWidget(self.team1_edit)
        layout.addWidget(self.team2_label)
        layout.addWidget(self.team2_edit)
        layout.addWidget(button_box)

        # self.setWindowFlags(Qt.WindowStaysOnTopHint)

    # Method to retrieve the entered team names
    def getTeamNames(self):
        return self.team1_edit.text(), self.team2_edit.text()
    
    # Method to center window
    def centerOnScreen(self):
        # Get the geometry of the screen
        screenGeo = QDesktopWidget().screenGeometry()

        # Move the dialog to the center of the screen
        self.move((screenGeo.width() - self.width()) // 2, (screenGeo.height() - self.height()) // 2)
