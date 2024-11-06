import sys
import os
import math

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from webFeedDialog import MyDialog
from constants import *
from opencv_main import OpenCVThread
from team_name import TeamNameDialog

from HelperFunctions.localCameras import get_available_cameras


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("BilliardsCV")

        self.setGeometry((MONITOR_WIDTH - WINDOW_WIDTH) // 2, math.floor(0.035 * MONITOR_HEIGHT), WINDOW_WIDTH,
                         WINDOW_HEIGHT)

        self.VBL = QHBoxLayout()

        self.FeedLabel = QLabel()

        button_width = 30
        button_height = 30
        button_spacing = 30

        # Helps switch names
        self.count = 0

        # Making lines to separate areas
        self.titleSectionLine = QFrame(self)
        self.titleSectionLine.setFrameShape(QFrame.VLine)
        self.titleSectionLine.setFrameShadow(QFrame.Sunken)
        self.titleSectionLine.setStyleSheet("border-width: 5px; border-style: solid;")
        self.titleSectionLine.setGeometry(math.floor(0.556 * WINDOW_WIDTH), 10, 2, WINDOW_HEIGHT)

        self.titleSectionLine = QFrame(self)
        self.titleSectionLine.setFrameShape(QFrame.HLine)
        self.titleSectionLine.setFrameShadow(QFrame.Sunken)
        self.titleSectionLine.setStyleSheet("border-width: 5px; border-style: solid;")
        self.titleSectionLine.setGeometry(math.floor(0.556 * WINDOW_WIDTH), math.floor(0.462 * WINDOW_HEIGHT),
                                          WINDOW_WIDTH // 2, 2)

        self.titleSectionLine = QFrame(self)
        self.titleSectionLine.setFrameShape(QFrame.HLine)
        self.titleSectionLine.setFrameShadow(QFrame.Sunken)
        self.titleSectionLine.setStyleSheet("border-width: 5px; border-style: solid;")
        self.titleSectionLine.setGeometry(math.floor(0.556 * WINDOW_WIDTH), math.floor(0.808 * WINDOW_HEIGHT),
                                          WINDOW_WIDTH // 2, 2)

        # Title Section
        self.titleSection = QLabel(self)
        self.titleSection.setText("Team Scores:")
        self.titleSection.setStyleSheet("color: black; font-size: 30px;")
        self.titleSection.setGeometry(100, 100, math.floor(0.278 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.titleSection.move(2 * WINDOW_WIDTH // 3, 10)

        # Team A section
        self.labelFrame = QFrame(self)
        self.labelFrame.setStyleSheet("border: 2px solid black;")
        self.labelFrame.setGeometry(100, 100, math.floor(0.067 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.labelFrame.move(math.floor(0.606 * WINDOW_WIDTH), math.floor(0.109 * WINDOW_HEIGHT))

        self.teamALabel = QLabel(self)
        self.teamALabel.setText("Team 1")
        self.teamALabel.setStyleSheet("color: black; font-size: 30px;")
        self.teamALabel.move(math.floor(0.611 * WINDOW_WIDTH), math.floor(0.115 * WINDOW_HEIGHT))

        self.teamAScore = QLabel(self)
        self.teamAScore.setText("Score: 0")
        self.teamAScore.setStyleSheet("color: black; font-size: 30px;")
        self.teamAScore.setGeometry(100, 100, math.floor(0.278 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.teamAScore.move(math.floor(0.606 * WINDOW_WIDTH), math.floor(0.154 * WINDOW_HEIGHT))

        self.teamABall = QLabel(self)
        self.teamABall.setText("Ball: ")
        self.teamABall.setStyleSheet("color: black; font-size: 30px;")
        self.teamABall.setGeometry(100, 100, math.floor(0.278 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.teamABall.move(math.floor(0.606 * WINDOW_WIDTH), math.floor(0.192 * WINDOW_HEIGHT))

        # + and - buttons for Team A
        self.teamAAddButton = QPushButton("-", self)
        self.teamAAddButton.clicked.connect(self.decrementTeamAScore)
        self.teamAAddButton.setGeometry(math.floor(0.583 * WINDOW_WIDTH), math.floor(0.185 * WINDOW_HEIGHT),
                                        button_width, button_height)

        self.teamASubtractButton = QPushButton("+", self)
        self.teamASubtractButton.clicked.connect(self.incrementTeamAScore)
        self.teamASubtractButton.setGeometry(math.floor(0.644 * WINDOW_WIDTH) + button_width + button_spacing,
                                             math.floor(0.185 * WINDOW_HEIGHT), button_width, button_height)

        # Team B section
        self.labelFrame = QFrame(self)
        self.labelFrame.setStyleSheet("border: 2px solid black;")
        self.labelFrame.setGeometry(100, 100, math.floor(0.067 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.labelFrame.move(math.floor(0.772 * WINDOW_WIDTH), math.floor(0.109 * WINDOW_HEIGHT))

        self.teamBLabel = QLabel(self)
        self.teamBLabel.setText("Team 2")
        self.teamBLabel.setStyleSheet("color: black; font-size: 30px;")
        self.teamBLabel.move(math.floor(0.778 * WINDOW_WIDTH), math.floor(0.115 * WINDOW_HEIGHT))

        self.teamBScore = QLabel(self)
        self.teamBScore.setText("Score: 0")
        self.teamBScore.setStyleSheet("color: black; font-size: 30px;")
        self.teamBScore.setGeometry(100, 100, math.floor(0.278 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.teamBScore.move(math.floor(0.772 * WINDOW_WIDTH), math.floor(0.154 * WINDOW_HEIGHT))

        self.teamBBall = QLabel(self)
        self.teamBBall.setText("Ball: ")
        self.teamBBall.setStyleSheet("color: black; font-size: 30px;")
        self.teamBBall.setGeometry(100, 100, math.floor(0.278 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.teamBBall.move(math.floor(0.772 * WINDOW_WIDTH), math.floor(0.192 * WINDOW_HEIGHT))

        # + and - buttons for Team B
        self.teamBAddButton = QPushButton("-", self)
        self.teamBAddButton.clicked.connect(self.decrementTeamBScore)
        self.teamBAddButton.setGeometry(math.floor(0.75 * WINDOW_WIDTH), math.floor(0.185 * WINDOW_HEIGHT),
                                        button_width, button_height)

        self.teamBSubtractButton = QPushButton("+", self)
        self.teamBSubtractButton.clicked.connect(self.incrementTeamBScore)
        self.teamBSubtractButton.setGeometry(math.floor(0.811 * WINDOW_WIDTH) + button_width + button_spacing,
                                             math.floor(0.185 * WINDOW_HEIGHT), button_width, button_height)

        # Switch player button
        self.switchPlayerButton = QPushButton("Switch", self)
        self.switchPlayerButton.clicked.connect(self.switchPlayers)
        self.switchPlayerButton.setGeometry(math.floor(0.7 * WINDOW_WIDTH), math.floor(0.4 * WINDOW_HEIGHT),
                                            math.floor(0.1 * WINDOW_WIDTH), math.floor(0.03 * WINDOW_HEIGHT))

        # Reset button
        self.resetResultButton = QPushButton("Reset", self)
        self.resetResultButton.clicked.connect(self.resetResult)
        self.resetResultButton.setGeometry(math.floor(0.85 * WINDOW_WIDTH), math.floor(0.4 * WINDOW_HEIGHT),
                                           math.floor(0.1 * WINDOW_WIDTH), math.floor(0.03 * WINDOW_HEIGHT))

        # Match status
        self.currentPlayerStatus = QLabel(self)
        self.currentPlayerStatus.setText("Current Player: player name from team 1")
        self.currentPlayerStatus.setStyleSheet("color: black; font-size: 30px;")
        self.currentPlayerStatus.setGeometry(100, 100, math.floor(0.389 * WINDOW_WIDTH),
                                             math.floor(0.077 * WINDOW_HEIGHT))
        self.currentPlayerStatus.move(math.floor(0.594 * WINDOW_WIDTH), math.floor(0.269 * WINDOW_HEIGHT))

        self.nextPlayerStatus = QLabel(self)
        self.nextPlayerStatus.setText("Next Player: player name from team 2")
        self.nextPlayerStatus.setStyleSheet("color: black; font-size: 30px;")
        self.nextPlayerStatus.setGeometry(100, 100, math.floor(0.389 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.nextPlayerStatus.move(math.floor(0.594 * WINDOW_WIDTH), math.floor(0.308 * WINDOW_HEIGHT))

        # Statistic
        self.hueStat = QLabel(self)
        self.hueStat.setText("Hue Adjustment:")
        self.hueStat.setStyleSheet("color: black; font-size: 30px;")
        self.hueStat.setGeometry(100, 100, math.floor(0.389 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.hueStat.move(math.floor(0.594 * WINDOW_WIDTH), math.floor(0.5 * WINDOW_HEIGHT))

        self.saturationStat = QLabel(self)
        self.saturationStat.setText("Saturation Adjustment:")
        self.saturationStat.setStyleSheet("color: black; font-size: 30px;")
        self.saturationStat.setGeometry(100, 100, math.floor(0.389 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.saturationStat.move(math.floor(0.594 * WINDOW_WIDTH), math.floor(0.592 * WINDOW_HEIGHT))

        self.saturationStat = QLabel(self)
        self.saturationStat.setText("Value Adjustment:")
        self.saturationStat.setStyleSheet("color: black; font-size: 30px;")
        self.saturationStat.setGeometry(100, 100, math.floor(0.389 * WINDOW_WIDTH), math.floor(0.077 * WINDOW_HEIGHT))
        self.saturationStat.move(math.floor(0.594 * WINDOW_WIDTH), math.floor(0.685 * WINDOW_HEIGHT))

        # Adding slider
        self.hueSlider = QSlider(Qt.Horizontal, self)
        self.hueSlider.setRange(-100, 100)
        self.hueSlider.setValue(0)
        self.hueSlider.setGeometry(100, 100, math.floor(0.167 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.hueSlider.move(math.floor(0.594 * WINDOW_WIDTH), math.floor(0.562 * WINDOW_HEIGHT))

        self.satSlider = QSlider(Qt.Horizontal, self)
        self.satSlider.setRange(-100, 100)
        self.satSlider.setValue(0)
        self.satSlider.setGeometry(100, 100, math.floor(0.167 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.satSlider.move(math.floor(0.594 * WINDOW_WIDTH), math.floor(0.654 * WINDOW_HEIGHT))

        self.valSlider = QSlider(Qt.Horizontal, self)
        self.valSlider.setRange(-100, 100)
        self.valSlider.setValue(0)
        self.valSlider.setGeometry(100, 100, math.floor(0.167 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.valSlider.move(math.floor(0.594 * WINDOW_WIDTH), math.floor(0.746 * WINDOW_HEIGHT))

        # Connect slider
        self.hueSlider.valueChanged.connect(self.updateHueNumber)
        self.satSlider.valueChanged.connect(self.updateSatNumber)
        self.valSlider.valueChanged.connect(self.updateValNumber)

        ## Store value
        self.huenumber = 0
        self.satnumber = 0
        self.valnumber = 0

        # Access value
        # print(self.hueSlider.value())
        # print(self.huenumber)

        # print(self.satSlider.value())
        # print(self.satnumber)

        # Display value on label
        self.huenumberLabel = QLabel(self)
        self.huenumberLabel.setText("0")
        self.huenumberLabel.setGeometry(100, 100, math.floor(0.167 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.huenumberLabel.move(math.floor(0.767 * WINDOW_WIDTH), math.floor(0.562 * WINDOW_HEIGHT))

        self.satnumberLabel = QLabel(self)
        self.satnumberLabel.setText("0")
        self.satnumberLabel.setGeometry(100, 100, math.floor(0.167 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.satnumberLabel.move(math.floor(0.767 * WINDOW_WIDTH), math.floor(0.654 * WINDOW_HEIGHT))

        self.valnumberLabel = QLabel(self)
        self.valnumberLabel.setText("0")
        self.valnumberLabel.setGeometry(100, 100, math.floor(0.167 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.valnumberLabel.move(math.floor(0.767 * WINDOW_WIDTH), math.floor(0.746 * WINDOW_HEIGHT))

        # mask settings
        self.checkbox = QCheckBox(self)
        self.checkbox.setGeometry(100, 100, math.floor(0.028 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.checkbox.move(math.floor(0.611 * WINDOW_WIDTH), math.floor(0.846 * WINDOW_HEIGHT))
        self.checkbox.stateChanged.connect(self.checkboxStateChanged)

        self.checkboxLabel = QLabel(self)
        self.checkboxLabel.setStyleSheet("color: black; font-size: 30px;")
        self.checkboxLabel.setText("Show Mask")
        self.checkboxLabel.setGeometry(100, 100, math.floor(0.167 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.checkboxLabel.move(math.floor(0.625 * WINDOW_WIDTH), math.floor(0.846 * WINDOW_HEIGHT))
        self.showMask = False

        # threshold stuff

        self.ThreshBox1 = QLineEdit(self)
        self.ThreshBox1.setGeometry(100, 100, math.floor(0.08 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.ThreshBox1.move(math.floor(0.6 * WINDOW_WIDTH), math.floor(0.9 * WINDOW_HEIGHT))
        self.ThreshBox1.setText(".25")
        self.ThreshButton1 = QPushButton(self)
        self.ThreshButton1.setGeometry(125, 125, math.floor(0.08 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.ThreshButton1.move(math.floor(0.6 * WINDOW_WIDTH), math.floor(0.95 * WINDOW_HEIGHT))
        self.ThreshButton1.setText("Stripe/Solid")
        self.ThreshButton1.clicked.connect(self.StripeSolidThresh)

        self.ThreshBox2 = QLineEdit(self)
        self.ThreshBox2.setGeometry(100, 100, math.floor(0.08 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.ThreshBox2.move(math.floor(0.75 * WINDOW_WIDTH), math.floor(0.9 * WINDOW_HEIGHT))
        self.ThreshBox2.setText("1.0")
        self.ThreshButton2 = QPushButton(self)
        self.ThreshButton2.setGeometry(125, 125, math.floor(0.08 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.ThreshButton2.move(math.floor(0.75 * WINDOW_WIDTH), math.floor(0.95 * WINDOW_HEIGHT))
        self.ThreshButton2.setText("Cue/Stripe")
        self.ThreshButton2.clicked.connect(self.CueStripeThresh)

        self.ThreshBox3 = QLineEdit(self)
        self.ThreshBox3.setGeometry(125, 125, math.floor(0.08 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.ThreshBox3.move(math.floor(0.9 * WINDOW_WIDTH), math.floor(0.9 * WINDOW_HEIGHT))
        self.ThreshBox3.setText(".8")
        self.ThreshButton3 = QPushButton(self)
        self.ThreshButton3.setGeometry(125, 125, math.floor(0.08 * WINDOW_WIDTH), math.floor(0.038 * WINDOW_HEIGHT))
        self.ThreshButton3.move(math.floor(0.9 * WINDOW_WIDTH), math.floor(0.95 * WINDOW_HEIGHT))
        self.ThreshButton3.setText("8ball")
        self.ThreshButton3.clicked.connect(self.EightThresh)

        # create the opencv thread
        self.Worker1 = OpenCVThread()
        self.Worker1.ImageUpdate.connect(self.image_update_slot)
        self.Worker1.BallInUpdate.connect(self.handleBallIn)

        self.FeedLabel = QLabel()

        program_path = os.path.join(os.path.dirname(__file__), "Resources", "default_pixmap_background.png")

        pic = QImage(program_path)
        pmap = pic.scaled(MAIN_FRAME_WIDTH, MAIN_FRAME_HEIGHT)
        self.FeedLabel.setPixmap(QPixmap.fromImage(pmap))

        self.FeedLabel.mouseReleaseEvent = self.Worker1.handleMouseClick
        self.FeedLabel.setGeometry(LEFT_MARGIN, MENU_BAR_HEIGHT, MAIN_FRAME_WIDTH, WINDOW_HEIGHT - MENU_BAR_HEIGHT)
        self.VBL.addWidget(self.FeedLabel)

        self.setupMenu()

        self.setTeamNames()

        self.setLayout(self.VBL)
        self.sizePolicy = QSizePolicy.Fixed

    def EightThresh(self):
        self.Worker1.setCueThresh(float(self.ThreshBox3.text()))
        print(float(self.ThreshBox3.text()))

    def CueStripeThresh(self):
        self.Worker1.setStripeThresh(float(self.ThreshBox2.text()))
        print(float(self.ThreshBox2.text()))

    def StripeSolidThresh(self):
        self.Worker1.setSolidThresh(float(self.ThreshBox1.text()))
        print(float(self.ThreshBox1.text()))

    def setupMenu(self):
        myQMenuBar = QMenuBar(self)
        settingsMenu = myQMenuBar.addMenu('Settings')

        feedMenu = settingsMenu.addMenu("Change Feed")
        localCamsMenu = feedMenu.addMenu("Local Cameras")
        localCamsMenu.aboutToShow.connect(lambda: self.addLocalCams(localCamsMenu))

        testAction = QAction("Web Feed", feedMenu)
        testAction.triggered.connect(lambda: self.show_dialog())
        feedMenu.addAction(testAction)

        testAction = QAction("Video File", feedMenu)
        testAction.triggered.connect(lambda: self.browseFiles())
        feedMenu.addAction(testAction)

        # videoOptionsMenu = settingsMenu.addMenu("Video Options")  # Will comment out for now until we implement
        # feature

        exitAction = QAction("Exit", settingsMenu)
        exitAction.triggered.connect(qApp.quit)
        settingsMenu.addAction(exitAction)

    def show_dialog(self):
        # Create and show the dialog
        dialog = MyDialog(self)
        result = dialog.exec_()

    def addLocalCams(self, menuToAdd):
        menuToAdd.clear()

        for camNum, camName in get_available_cameras().items():
            localCamAction = QAction(camName, menuToAdd)
            localCamAction.triggered.connect(lambda checked, feed=camNum: self.setVideoFeed(feed))
            menuToAdd.addAction(localCamAction)

    # Placer methods to manually update score using buttons

    def incrementTeamAScore(self):
        current_score = int(self.teamAScore.text().split(":")[1])
        new_score = current_score + 1
        self.teamAScore.setText(f"Score: {new_score}")

    def decrementTeamAScore(self):
        current_score = int(self.teamAScore.text().split(":")[1])
        new_score = max(0, current_score - 1)
        self.teamAScore.setText(f"Score: {new_score}")

    def incrementTeamBScore(self):
        current_score = int(self.teamBScore.text().split(":")[1])
        new_score = current_score + 1
        self.teamBScore.setText(f"Score: {new_score}")

    def decrementTeamBScore(self):
        current_score = int(self.teamBScore.text().split(":")[1])
        new_score = max(0, current_score - 1)
        self.teamBScore.setText(f"Score: {new_score}")

    def assignSolidBall(self):
        current_team = self.currentPlayerStatus.text().split(":")[1]
        if current_team == " " + self.teamALabel.text():
            self.teamABall.setText("Ball: Solid")
            self.teamBBall.setText("Ball: Stripe")
        elif current_team == " " + self.teamBLabel.text():
            self.teamBBall.setText("Ball: Solid")
            self.teamABall.setText("Ball: Stripe")

    def assignStripeBall(self):
        current_team = self.currentPlayerStatus.text().split(":")[1]
        if current_team == " Team A":
            self.teamABall.setText("Ball: Stripe")
            self.teamBBall.setText("Ball: Solid")
        elif current_team == " Team B":
            self.teamBBall.setText("Ball: Stripe")
            self.teamABall.setText("Ball: Solid")

    def handleBallIn(self, ballType, firstBall):
        if ballType == BALL_TYPE_SOLID:
            if firstBall:
                self.assignSolidBall()
            current_team = self.teamABall.text().split(":")[1]
            current_team2 = self.teamBBall.text().split(":")[1]
            # print(current_team)
            # print(current_team2)
            if current_team == " Solid":
                # print(current_team)
                self.incrementTeamAScore()
            elif current_team2 == " Solid":
                # print(current_team2)
                self.incrementTeamBScore()
        elif ballType == BALL_TYPE_STRIPE:
            if firstBall:
                self.assignStripeBall()
            current_team = self.teamABall.text().split(":")[1]
            current_team2 = self.teamBBall.text().split(":")[1]
            # print(current_team)
            # print(current_team2)
            if current_team == " Stripe":
                # print(current_team)
                self.incrementTeamAScore()

            elif current_team2 == " Stripe":
                # print(current_team2)
                self.incrementTeamBScore()

    # Open a dialog to set team names and update associated labels
    def setTeamNames(self):
        # Open a dialog to get team names
        team_dialog = TeamNameDialog(self)
        if team_dialog.exec_():
            # Retrieve team names from the dialog
            teamA, teamB = team_dialog.getTeamNames()

            # Set team names labels
            self.teamALabel.setText(teamA)
            self.teamBLabel.setText(teamB)

            # Update player status labels
            self.updatePlayerStatus(teamA, teamB)

    # Switch between current and next players' team names and update labels
    def switchPlayers(self):
        # Get current team names
        teamA = self.teamALabel.text()
        teamB = self.teamBLabel.text()
        if self.count == 0:

            # Swap team names and update player status
            self.updatePlayerStatus(teamB, teamA)

            # Toggle the count for the next switch
            self.count = 1

        else:
            self.updatePlayerStatus(teamA, teamB)
            self.count = 0

    # Reset all result
    def resetResult(self):
        self.teamAScore.setText("Score: 0")
        self.teamBScore.setText("Score: 0")
        self.teamABall.setText("Ball: ")
        self.teamBBall.setText("Ball: ")
        self.currentPlayerStatus.setText("Current player: ")
        self.nextPlayerStatus.setText("Next player:")
        self.handleBallIn

    # Update labels with current and next player information
    def updatePlayerStatus(self, current_team, next_team):
        # Set labels for current and next players
        self.currentPlayerStatus.setText(f"Current Player: {current_team}")
        self.nextPlayerStatus.setText(f"Next Player: {next_team}")

    def updateHueNumber(self, value):
        self.huenumber = value
        self.huenumberLabel.setText(str(value))
        self.Worker1.setHueAdjust(value)

    def updateSatNumber(self, value):
        self.satnumber = value
        self.satnumberLabel.setText(str(value))
        self.Worker1.setSaturationAdjust(value)

    def updateValNumber(self, value):
        self.valnumber = value
        self.valnumberLabel.setText(str(value))
        self.Worker1.setValueAdjust(value)

    def image_update_slot(self, frame, useMainFrame):
        width = MAIN_FRAME_WIDTH if useMainFrame else WARPED_FRAME_WIDTH
        height = MAIN_FRAME_HEIGHT if useMainFrame else WARPED_FRAME_HEIGHT

        cv2.cvtColor(frame, cv2.COLOR_HSV2RGB, dst=frame)
        self.FeedLabel.setPixmap(QPixmap.fromImage(
            QImage(frame.data, frame.shape[1], frame.shape[0], 3 * frame.shape[1], QImage.Format_RGB888).scaled(width,
                                                                                                                height)))

    def checkboxStateChanged(self):
        self.showMask = not self.showMask
        self.Worker1.setMaskVisible(self.showMask)

    def browseFiles(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '',
                                                   'Video Files (*.mp4 *.mov *.wmv *.avi *.mpg *.mpeg)')

        if file_name:
            self.setVideoFeed(file_name)

    def setVideoFeed(self, feed):
        self.Worker1.setCaptureSource(feed)

        if not self.Worker1.isActive():
            self.Worker1.start()

    def keyReleaseEvent(self, event):
        self.Worker1.handleKeyPress(event)

    def cancel_feed(self):
        self.Worker1.stop()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    App.setWindowIcon(QIcon("Resources/8ball.png"))

    Root = MainWindow()
    Root.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    Root.setContentsMargins(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    Root.show()
    sys.exit(App.exec())
