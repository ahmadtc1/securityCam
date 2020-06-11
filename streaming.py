from computerVision.motionDetector import singleMotionDetector
import numpy as np
from flask import Flask, render_template, Response
import threading
import argparse
import datetime
import time
from imutils.video import VideoStream
import cv2


#Init a lock for thread safety when exchanging output frames
outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

#Start the video stream and let it sleep for 2 seconds so the camera can warm up
vs = VideoStream(src=0).start()
time.sleep(2.0)

#Default path routing
@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

def detectMotion(frameCount:
    #Obtain global refs to the videostream, output frame, and lock
    global vs, outputFrame, lock

    md = singleMotionDetector(accumWeigh=0.1)
    total = 0


if (__name__ == "__main__"):
    app.run()