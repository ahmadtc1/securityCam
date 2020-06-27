import numpy as np
import imutils
import cv2
import datetime
from requests_oauthlib import OAuth1
import requests

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
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
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

        if ((lowerX, lowerY) == (np.inf, np.inf) and (upperX, upperY) == (-np.inf, -np.inf)):
            time = datetime.datetime.now()
            url = 'https://api.twitter.com/1.1/direct_messages/events/new.json'
            message = "Motion has been detected on youe camera stream at " + time.strftime("%A %d %B %Y %I:%M:%S%p")
            auth = OAuth1('OJCwZkO2oHJ9KkxBuRz9PQyOa', 'Ws5aJZANI6tVw53nEvCl7B5cyceB6N8wqhdD3hPluy7IXkPd0t',
            '3324006958-ppFpnkIC7MHMBH3WsJHOZKCk7aaEJnVhtm5y3Hi', '9k3Nc9INYHC4qbQj4xcTl7VRHsArXegoFqOXdKDZ6v48j')
            headers = {'content-type': 'application/json'}
            payload = {
                "event": {
                    "type": "message_create",
                    "message_create": {
                        "target": {
                            "recipient_id": "3324006958"
                        },
                        "message_data": {
                            "text": message
                        }
                    }
                }
            }
            

            response = requests.post(url, headers=headers, data=payload)

        return (thresh, (lowerX, lowerY, upperX, upperY))
