from computerVision.motionDetector import singleMotionDetector as smd
import numpy as np
from flask import Flask, render_template, Response
import threading
import argparse
import datetime
import time
from imutils.video import VideoStream
import cv2
import imutils

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

def detectMotion(frameCount):
    #Obtain global refs to the videostream, output frame, and lock
    global vs, outputFrame, lock

    md = smd.SingleMotionDetector(accumulativeWeight=0.1)
    total = 0

    while True:
        #Obtain the frame and greyscale and slightly blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        #Obtain the timestamp and add it to the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
        if (total > frameCount):
            #If sufficient frames have come by, detect for motion
            motion = md.detect(gray)

            if (motion is not None):
                #If motion was found, display where the motion occurred
                (thresh, (lowerX, lowerY, upperX, upperY)) = motion
                cv2.rectangle(frame, (lowerX, lowerY), (upperX, upperY), (0, 0, 255), 2)
        
        #Update the background and increment tht total num of frames
        md.update(gray)
        total += 1

        #Ensure the outputFrame is not being read while also being updated
        #and copy it to the output frame
        with lock:
            outputFrame = frame.copy()

def generate():
    #Obtain global refs to the lock and outputFrame
    global outputFrame, lock

    #Loop over the output stream frames
    while True:
        #Acquire the lock so that outputframe is not read while being updated
        with lock:
            #If the outputframe isn't set, continue looping
            if (outputFrame is None):
                continue

            (succesfullyEncoded, encodedImg) = cv2.imencode(".jpg", outputFrame)

            #If the image wasn't succesfully encoded, continue looping
            if (not succesfullyEncoded):
                continue

        #Yield the output frame in a byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImg) + b'\r\n')


@app.route("/video_stream", methods=["GET"])
def videoStream():
    #Return the generated response along with the media type
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


if (__name__ == "__main__"):
    #Build the argument parser for the cli
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", help="ip address of the device", 
        type=str, required=True)
    ap.add_argument("-o", "--port", help="port of the server (1024 to 65535",
        type=int, required=True)
    ap.add_argument("-f", "--frame_count", help="minimum number of frames required to form background",
        type=int, default=32)
    args = vars(ap.parse_args())

    #Set up the threading for concurrency handling
    t = threading.Thread(target=detectMotion, args=(args["frame_count"],))
    t.daemon = True
    t.start()


    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)

vs.stop()