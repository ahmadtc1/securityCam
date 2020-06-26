import numpy as np
import argparse
import cv2
import datetime
import imutils
import os

class FaceDetector:
    def __init__(self, prototxt, model):
        self.prototxt = prototxt
        self.model = model
        self.loadModel()

    def loadModel(self):
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

    def detectFaces(self, image):
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300,300)), 1.0, (300,300), (104.0,177.0,123.0))
        self.net.setInput(blob)
        detections = self.net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0,0,i,2]
            if (confidence > 0.5):
                box = detections[0,0,i,3:7] * np.array([w,h,w,h])
                (startX, startY, endX, endY) = box.astype("int")
                width = endX - startX
                height = endY - startY

                face = image[startY: endY, startX: endX]
                #face = imutils.resize(face, width = width + 100)
                #cv2.rectangle(image, (startX, startY), (endX, endY), (0,0,255), 2)
                self.saveImg(face)


    def saveImg(self, image):
        #If it doesn't already exist, create a directory for storing the detected faces
        if (not os.path.isdir("faces")):
            os.mkdir("faces")

        #Construct the fileName for each detected face using a timestamp
        now = datetime.datetime.now()
        current_time = now.strftime("%H.%M.%S")
        fileName = current_time + " - detected" + ".jpg"
        i = 0
        # If the file already exists, we keep looping to define a unique 
        # filename using index as unique identifier

        while (os.path.isfile(os.path.join("faces", fileName))):
            fileName = current_time + " - detected (" + str(i) + ")" + ".jpg"
            i += 1

        filePath = os.path.join("faces", fileName)

        cv2.imwrite(filePath, image)
