from constants import *


class Ball:
    #Class which holds information about the balls
    def __init__(self, pos, vel):
        self.position = pos
        self.velocity = vel
        self.life = 1

        # tracks the highest average ball type
        self.ballType = BALL_TYPE_UNKNOWN

        # counts for each type of ball
        self.cueCount = 0
        self.eightCount = 0
        self.stripedCount = 0
        self.solidCount = 0


class BallTracker:
    #The main tracker class, uses a Euclidian distance tracker to identify the balls across multiple frames
    def __init__(self):
        self.balls = {}
        self.potentials = {}
        self.id_count = 0

    def update(self, objects_rect):
        #Takes in an array of rectangles which bound the detected balls, and updates the tracking information
        #accordingly. Also updates the dictionary of balls which could potentially go in.
        new_balls = {}
        self.potentials = {}

        for rect in objects_rect:
            x, y, w, h, ballType = rect
            midpoint = [x + w // 2, y + h // 2]
            curr_id = None

            # find out if that ball was detected already in the last frame
            same_object_detected = False
            for id in self.balls:
                ball = self.balls[id]
                distance = dist(ball.position, midpoint)

                if distance < 50:
                    ball.velocity = [midpoint[0] - ball.position[0], midpoint[1] - ball.position[1]]
                    ball.position = midpoint
                    ball.life += 1
                    new_balls[id] = ball

                    # adds to a type of ball's count depending on the passed type value
                    if ballType == BALL_TYPE_EIGHT:
                        ball.eightCount += 1
                    elif ballType == BALL_TYPE_CUE:
                        ball.cueCount += 1
                    elif ballType == BALL_TYPE_STRIPE:
                        ball.stripedCount += 1
                    elif ballType == BALL_TYPE_SOLID:
                        ball.solidCount += 1

                    # sets ball type to the count with the greatest value
                    if ((ball.eightCount > ball.cueCount) and (ball.eightCount > ball.stripedCount) and (
                            ball.eightCount > ball.solidCount)):
                        ball.ballType = BALL_TYPE_EIGHT
                    if ((ball.cueCount > ball.eightCount) and (ball.cueCount > ball.stripedCount) and (
                            ball.cueCount > ball.solidCount)):
                        ball.ballType = BALL_TYPE_CUE
                    if ((ball.stripedCount > ball.eightCount) and (ball.stripedCount > ball.cueCount) and (
                            ball.stripedCount > ball.solidCount)):
                        ball.ballType = BALL_TYPE_STRIPE
                    if ((ball.solidCount > ball.eightCount) and (ball.solidCount > ball.cueCount) and (
                            ball.solidCount > ball.stripedCount)):
                        ball.ballType = BALL_TYPE_SOLID

                    curr_id = id
                    same_object_detected = True
                    break

            # This is a new object that was not detected in the last frame
            if not same_object_detected:
                new_balls[self.id_count] = Ball(midpoint, [0, 0])
                curr_id = self.id_count
                self.id_count += 1

            if curr_id is None:
                print("This error should not occur")

            updated_ball = new_balls[curr_id]
            pocket, distance = getClosestPocketAndDistance([x, y, w, h])

            if distance < 3 * POCKET_RADIUS / 4:
                self.potentials[curr_id] = updated_ball

        self.balls = new_balls.copy()

    def found(self, key):
        #Returns whether a particular key is found in the dictionary of balls
        return key in self.balls

    def getPotentials(self):
        #Returns the balls that could potentially go in at any particular time
        return self.potentials

    def getBalls(self):
        return self.balls

    def printAll(self):
        for key in self.balls:
            ball = self.balls[key]
            print("Id: " + str(key) + " pos: " + str(ball.position) + " vel: " + str(ball.velocity))
            print("")

    def getBallInfo(self):
        ballList = []
        for key in self.balls:
            ball = self.balls[key]
            ballList.append([key, ball.ballType])
        return ballList


def dot(vec1, vec2):
    # dot product of 2 2d vectors
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

def vectorAvgNorm(vec1, vec2):
    # normalized average of two vectors
    vec = [(vec1[0] + vec2[0]) / 2, (vec1[1] + vec2[1]) / 2]
    normalize(vec)
    return vec

def valueInRange(val, low, high):
    # returns true if val is between low and high
    if val >= low and val <= high:
        return True
    return False

def magnitude(vec):
    # 2d vector magnitude
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])

def normalize(vec):
    # normalizes a vector
    mag = magnitude(vec)
    if mag > 0:
        vec[0] /= mag
        vec[1] /= mag


def dist(pt1, pt2):
    #Euclidian distance function between two points
    return math.sqrt((pt1[0] - pt2[0]) * (pt1[0] - pt2[0]) + (pt1[1] - pt2[1]) * (pt1[1] - pt2[1]))


def getClosestPocketAndDistance(rect):
    #Given a bounding box 'rect', returns the location of the closest pocket and the distance
    #to that pocket
    midpoint = (rect[0] + math.floor(rect[2] / 2), rect[1] + math.floor(rect[3] / 2))
    min_dist = 10000000
    closest_pocket = None
    for pocket in WARPED_FRAME_POCKETS:
        distance = dist(midpoint, pocket)
        if distance < min_dist:
            min_dist = distance
            closest_pocket = pocket
    return closest_pocket, min_dist
