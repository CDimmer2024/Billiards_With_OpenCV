from PyQt5.QtCore import *

import numpy as np

from tracker import *
object_detector = cv2.createBackgroundSubtractorMOG2(history=75, varThreshold=0, detectShadows=True)
#object_detector2 = cv2.createBackgroundSubtractorKNN(history=75, detectShadows=True)

class OpenCVThread(QThread):
    ImageUpdate = pyqtSignal((np.ndarray, bool))
    BallInUpdate = pyqtSignal((int, bool))
    ThreadActive = False
    in_table_setup = True
    pockets = ["top left", "middle left", "bottom left", "top right", "middle right", "bottom right"]
    pocketLocations = []
    keyPressQueue = []
    hueAdjust = 0
    saturationAdjust = 0
    valueAdjust = 0
    capture = None
    paused = False
    maskVisible = False

    EightThresh = EIGHT_THRESHOLD
    CueStripeThresh = CUE_STRIPE_THRESHOLD
    StripeSolidThresh = STRIPE_SOLID_THRESHOLD

    def setEightThresh(self, newThresh):
        self.EightThresh = newThresh

    def setCueThresh(self, newThresh):
        self.CueThresh = newThresh

    def setSolidThresh(self, newThresh):
        self.SolidThresh = newThresh
    
    def setStripeThresh(self, newThresh):
        self.StripeThresh = newThresh

    def setCaptureSource(self, source):
        if self.capture is not None:
            self.capture.release()
        self.capture = cv2.VideoCapture(source)

    def handleMouseClick(self, event):
        if not self.ThreadActive:
            return

        x = event.x()
        y = event.y() if not self.in_table_setup else event.y() - math.floor((WINDOW_HEIGHT - MAIN_FRAME_HEIGHT)/2)
        if x > MAIN_FRAME_WIDTH or y > MAIN_FRAME_HEIGHT or y < 0:
            return

        if event.button() == Qt.MouseButton.LeftButton and len(self.pocketLocations) < 6:
            self.pocketLocations.append([x, y+MENU_BAR_HEIGHT//2])
        elif event.button() == Qt.MouseButton.RightButton and len(self.pocketLocations) > 0:
            self.pocketLocations.pop()

    def handleKeyPress(self, event):
        if not self.ThreadActive:
            return

        if event.text() == "p":
            self.paused = not self.paused
        else:
            self.keyPressQueue.append(event.text())

    def setHueAdjust(self, hueValue):
        self.hueAdjust = hueValue

    def setSaturationAdjust(self, satValue):
        self.saturationAdjust = satValue

    def setValueAdjust(self, valValue):
        self.valueAdjust = valValue

    def setMaskVisible(self, isVisible):
        self.maskVisible = isVisible

    def run(self):
        if self.capture is None:
            return

        self.ThreadActive = True
        while self.ThreadActive:

            self.tableSetup()

            frame = self.capture.read()[1]
            warped = self.getWarpedFrame(frame)
            self.drawPockets(warped)
            while (not self.ensureTableCorrect(warped)):

                # reset pocketsLocations to empty
                self.pocketLocations = []
                # re-run table setup
                self.tableSetup()
                # grab new frame
                frame = self.capture.read()[1]
                warped = self.getWarpedFrame(frame)
                self.drawPockets(warped)

            self.ballTracking()


    def stop(self):
        self.ThreadActive = False
        self.quit()

    def isActive(self):
        return self.ThreadActive

    def tableSetup(self):
        #function responsible for the initial table setup portion of the program, populates the array of pocketLocations
        #for use in frame warping later in the program
        frame = self.capture.read()[1]
        cleanFrame = np.copy(frame)  # Note: cleanFrame is necessary to redraw things on the frame while paused

        # this function runs ridiculously fast, use this counter so we are not sending a massive
        # number of image updates to the main gui thread
        iterationCounter = 0

        while True:

            frame = np.copy(cleanFrame)

            if not self.paused:
                if len(self.pocketLocations) == 6:
                    break
                ret, frame = self.capture.read()
                if not ret:
                    continue
                cleanFrame = np.copy(frame)

            height2, width2, _ = frame.shape
            # draw things on the frame
            for pt in self.pocketLocations:
                newpt = [math.floor(pt[0]/MAIN_FRAME_WIDTH*width2), math.floor(pt[1]/MAIN_FRAME_HEIGHT*height2)]
                cv2.circle(frame, newpt, 5, (255, 0, 0), -1)

            line1TextLocation = (math.floor(width2 / 2) - 150, math.floor(height2 / 2) - 20)
            line2TextLocation = (line1TextLocation[0] - 100, line1TextLocation[1] + 50)

            if self.paused:
                if len(self.pocketLocations) < 6:
                    cv2.putText(frame, "Click " + self.pockets[len(self.pocketLocations)] + " pocket", line1TextLocation, FONT, 1,
                                (255, 0, 0), 2)
                else:
                    bounds = self.getTableBounds(width2, height2)
                    cv2.polylines(frame, [bounds], True, (255, 0, 0), 5)
                    cv2.putText(frame, "Press 'p' to un-pause", line1TextLocation, FONT, 1, (255, 0, 0), 2)

                cv2.putText(frame, "Right-click to remove last point", line2TextLocation, FONT, 1, (255, 0, 0), 2)
            else:
                cv2.putText(frame, "Press 'p' select pockets", line1TextLocation, FONT, 1, (255, 0, 0), 2)

            #only send every fifth image, otherwise it blocks the main thread
            #because we get so many updates
            if self.paused:
                iterationCounter += 1
                if iterationCounter >= 5:
                    iterationCounter = 0
                    self.sendImage(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), True)
            else:
                self.sendImage(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), True)

    def getTableBounds(self, framewidth, frameheight):
        #Extracts the bounds of the table, scaled apropriately for the frame size
        if len(self.pocketLocations) != 6:
            Exception("errant call of getTableBounds")

        topLeft = (self.pocketLocations[0][0], self.pocketLocations[0][1])
        bottomLeft = (self.pocketLocations[2][0], self.pocketLocations[2][1])
        bottomRight = (self.pocketLocations[5][0], self.pocketLocations[5][1])
        topRight = (self.pocketLocations[3][0], self.pocketLocations[3][1])

        scalefactx = MAIN_FRAME_WIDTH
        scalefacty = MAIN_FRAME_HEIGHT

        topLeft = [math.floor(topLeft[0]/scalefactx*framewidth), math.floor(topLeft[1]/scalefacty*frameheight)]
        bottomLeft = [math.floor(bottomLeft[0]/scalefactx*framewidth), math.floor(bottomLeft[1]/scalefacty*frameheight)]
        bottomRight = [math.floor(bottomRight[0]/scalefactx*framewidth), math.floor(bottomRight[1]/scalefacty*frameheight)]
        topRight = [math.floor(topRight[0]/scalefactx*framewidth), math.floor(topRight[1]/scalefacty*frameheight)]

        return np.array([topLeft, bottomLeft, bottomRight, topRight])

    def sendImage(self, frame, inTableSetup):
        #Function sends an image to the main GUI thread, inTableSetup is
        #a boolean which tells us whether we are sending the un-modified frame (True),
        #or the warped frame (False)
        self.ImageUpdate.emit(frame, inTableSetup)

    def drawCountourBoxes(self, warpedframe):
        #This is the main function responsible for the ball detection,
        #It begins by masking the table, then extracting countours, then checking
        #Which types of balls are detected, draws the contour boxes and returns an array of
        #The balls which were detected
        detections = []
        warpedFramArea = WARPED_FRAME_WIDTH * WARPED_FRAME_HEIGHT

        mask = object_detector.apply(warpedframe)
        cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY, dst=mask)
        kernel = np.ones((3, 3), np.uint8)
        cv2.erode(mask, kernel, dst=mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:

            area = cv2.contourArea(cnt)
            #aribitrary sizes that seem to work for  the balls
            if area > warpedFramArea/3000 and area < warpedFramArea/300:

                middle, dims, angle = cv2.minAreaRect(cnt)
                aspect_ratio = dims[0] / dims[1]
                if aspect_ratio < 0.5 or aspect_ratio > 2:
                    continue

                x,y,w,h = cv2.boundingRect(cnt)
                detections.append([x, y, w, h])
                (cx, cy), radius = cv2.minEnclosingCircle(cnt)
                cv2.circle(mask, (math.floor(cx), math.floor(cy)), math.floor(radius), 255, -1)

        cv2.cvtColor(warpedframe, cv2.COLOR_BGR2HSV, dst=warpedframe)
        h, s, v = cv2.split(warpedframe)

        h = h.astype(np.float32)
        s = s.astype(np.float32)
        v = v.astype(np.float32)

        # Perform adjustments in-place
        h *= (1 + self.hueAdjust / 100)
        s *= (1 + self.saturationAdjust / 100)
        v *= (1 + self.valueAdjust / 100)

        # Clip values in-place
        np.clip(h, 0, 179, out=h)
        np.clip(s, 0, 255, out=s)
        np.clip(v, 0, 255, out=v)

        # Merge channels and convert back to BGR in-place
        cv2.merge([h.astype(np.uint8), s.astype(np.uint8), v.astype(np.uint8)], dst=warpedframe)

        for ball in detections:
            x,y,w,h = ball

            cv2.rectangle(warpedframe, (x, y), (x + w, y + h), (36, 255, 12), 1)
            reduced = warpedframe[y:y + h, x:x + w]

            green = [130, 158, 0]

            diff = 100

            boundaries = [
                ([green[2], green[1] - diff, green[0] - diff], [green[2] + diff, green[1] + diff, green[0] + diff])]

            percent = 0

            for (lower, upper) in boundaries:
                ##WHITE CHECKER
                lowerValues = np.array([0, 0, 168])
                upperValues = np.array([172, 111, 255])

                hsvMask = cv2.inRange(reduced, lowerValues, upperValues)

                ratio_white = cv2.countNonZero(hsvMask) / (reduced.size * 10)

                colorPercent = (ratio_white * 100)

                whitePercent = np.round(colorPercent, 2)

                # BLACK CHECKER
                lowerValuesBLACK = np.array([0, 0, 0])
                upperValuesBLACK = np.array([172, 225, 40])

                hsvMask2 = cv2.inRange(reduced, lowerValuesBLACK, upperValuesBLACK)

                ratio_black = cv2.countNonZero(hsvMask2) / (reduced.size * 10)

                colorPercentBLACK = (ratio_black * 100)

                blackPercent = np.round(colorPercentBLACK, 2)

            if (blackPercent > self.EightThresh):
                cv2.putText(warpedframe, "8ball: " + blackPercent.astype('str'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cv2.mean(area), 2)
                ball.append(BALL_TYPE_EIGHT)
            else:
                if (whitePercent > self.CueStripeThresh):
                    cv2.putText(warpedframe, "Cue ball: " + whitePercent.astype('str'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cv2.mean(area), 2)
                    ball.append(BALL_TYPE_CUE)
                elif (whitePercent > self.StripeSolidThresh):
                    cv2.putText(warpedframe, "Striped: " + whitePercent.astype('str'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cv2.mean(area), 2)
                    ball.append(BALL_TYPE_STRIPE)
                elif (whitePercent <= self.StripeSolidThresh):
                    cv2.putText(warpedframe, "Solid: " + whitePercent.astype('str'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cv2.mean(area), 2)
                    ball.append(BALL_TYPE_SOLID)
                else:
                    cv2.putText(warpedframe, percent.astype('str'), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, cv2.mean(area), 2)
                    ball.append(BALL_TYPE_UNKNOWN)

        if self.maskVisible:
            result = cv2.bitwise_and(warpedframe, warpedframe, mask=mask)
            # Update the original image with the result
            np.copyto(warpedframe, result)

        return detections

    def dist(self, pt1, pt2):
        #Euclidian distance between two points
        return math.sqrt((pt1[0] - pt2[0]) * (pt1[0] - pt2[0]) + (pt1[1] - pt2[1]) * (pt1[1] - pt2[1]))

    def getWarpedFrame(self, frame):
        # takes in the frame and returns the warped version of the frame to a 2:1 aspect ratio rectangle
        height, width, _ = frame.shape
        tableVerts = self.getTableBounds(width, height)

        rect_coords = np.array([[POCKET_RADIUS, POCKET_RADIUS], [POCKET_RADIUS, WARPED_FRAME_HEIGHT-POCKET_RADIUS], [WARPED_FRAME_WIDTH-POCKET_RADIUS, WARPED_FRAME_HEIGHT-POCKET_RADIUS], [WARPED_FRAME_WIDTH-POCKET_RADIUS, POCKET_RADIUS]], np.float32)
        M = cv2.getPerspectiveTransform(tableVerts.astype(np.float32), rect_coords)

        rect_homog = np.array([[0, 0, 1], [0, WARPED_FRAME_HEIGHT, 1], [WARPED_FRAME_WIDTH, WARPED_FRAME_HEIGHT, 1], [WARPED_FRAME_WIDTH, 0, 1]], np.float32)
        M_inv = np.linalg.inv(M)

        for i in range(0, len(rect_homog)):
            point = M_inv.dot(rect_homog[i])
            tableVerts[i] = [point[0] / point[2], point[1] / point[2]]

        blank = np.zeros(frame.shape[:2], dtype='uint8')
        mask = cv2.fillPoly(blank, [tableVerts], 255)
        masked = cv2.bitwise_and(frame, frame, mask=mask)
        return cv2.warpPerspective(masked, M, (WARPED_FRAME_WIDTH, WARPED_FRAME_HEIGHT))

    def drawPockets(self, warpedframe):
        # draws a semicircle around each pocket for help in the setup screen
        for pocket in WARPED_FRAME_POCKETS:
            cv2.circle(warpedframe, pocket, POCKET_RADIUS, 255, 10)

    def ensureTableCorrect(self, warpedframe):
        #Prompts the user to specify whether the table was setup correctly, returns True if correct,
        #False otherwise
        cv2.putText(warpedframe, "Are all pockets", (math.floor(WARPED_FRAME_WIDTH / 2) - 120, math.floor(WARPED_FRAME_HEIGHT / 2) - 50),
                    FONT, 1,
                    (255, 0, 0), 2)
        cv2.putText(warpedframe, "aligned correctly", (math.floor(WARPED_FRAME_WIDTH / 2) - 130, math.floor(WARPED_FRAME_HEIGHT / 2) - 25),
                    FONT,
                    1, (255, 0, 0), 2)
        cv2.putText(warpedframe, "(y/n)", (math.floor(WARPED_FRAME_WIDTH / 2) - 50, math.floor(WARPED_FRAME_HEIGHT / 2)), FONT, 1, (255, 0, 0), 2)
        self.sendImage(cv2.cvtColor(warpedframe, cv2.COLOR_BGR2HSV), False)
        self.keyPressQueue = []
        while len(self.keyPressQueue) == 0: continue
        key = self.keyPressQueue.pop(0)
        if key == 'y' or key == 'Y':
            return True
        else:
            return False


    def ballTracking(self):
        #euclidian distance tracker from pySource
        my_tracker = BallTracker()

        #dictionaries of the balls that could go in for this frame and the last frame
        potentials_curr = {}
        potentials_prev = {}
        balls_in = 0

        while True:
            ret, frame = self.capture.read()
            if not ret:
                self.ThreadActive = False
                break

            warped = self.getWarpedFrame(frame)
            detected_balls = self.drawCountourBoxes(warped)
            self.drawPockets(warped)

            #get the ids of the boxes for euclidian distance tracker
            my_tracker.update(detected_balls)

            potentials_curr = my_tracker.getPotentials()

            if potentials_prev:
                for key in potentials_prev:
                    #if that potential made ball is no longer found, increment the made balls
                    if key not in potentials_curr and not my_tracker.found(key) and potentials_prev[key].life > 3:
                        balls_in += 1
                        print("Ball Pocketed " + str(balls_in))
                        self.BallInUpdate.emit(potentials_prev[key].ballType, True if balls_in == 1 else False)
            
            self.sendImage(warped, False)
            potentials_prev = potentials_curr

            #for debugging purposes, control video feed with button press
            # while len(self.keyPressQueue) == 0:
            #     continue
            # while len(self.keyPressQueue) > 0:
            #     self.keyPressQueue.pop(0)
