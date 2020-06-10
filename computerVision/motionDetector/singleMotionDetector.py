import numpy as np
import imutils
import cv2

class SingleMotionDetector:

    #initialize with accumulative weight and set background to none
    def __init__(self, accumulativeWeight=0.5):
        #Setting accumWeight to 0.5 initially to evenly weigh the initial bg
        self.accumWeight = accumulativeWeight
        self.bg = None

    def update(self, image):
        #Initialize the bg if it hasn't been set yet
        if (self.bg is None):
            self.bg = image.copy().astype("float")
            return
        #Calculate the weighted average
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, threshVal=25):
        #Calculate the difference between the background and the current image and thresh it
        delta = cv2.absdiff(self.bg.astype("float"), image)
        thresh = cv2.threshold(delta, threshVal, 255, cv2.THRESH_BINARY)[1]

        #erode and dilate to clean up contours
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        #Grab the contours from the threshed image
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        #Initialize (x, y) coords for the corners of the motion
        (lowerX, lowerY) = (np.inf, np.inf)
        (upperX, upperY) = (-np.inf, -np.inf)

        if (len(contours) == 0):
            return None
        
        #Update the area of motion dependant on the area of the motion contours
        for cont in contours:
            (x, y, w, h) = cv2.boundingRect(cont)
            (lowerX, lowerY) = (min(lowerX, x), min(lowerY, y))
            (upperX, upperY) = (max(upperX, x + w), max(upperY, y + h))

        return (thresh, (lowerX, lowerY, upperX, upperY))
