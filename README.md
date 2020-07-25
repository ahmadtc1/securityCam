
# securityCam

🎥 A real-time camera streaming application with motion detection alerts and face-detection

  

## What is it?

securityCam is a real-time security camera application built on a **flask** server to stream video from a **Raspberry Pi** to the internet. Motion detection was implemented using **OpenCV** to issue alerts through the **Twitter API** when motion is detected. Face detection was also implemented to detect and save any faces found in the stream. Check out some technical details regarding the different features below :)
  
  

## More on the Motion Detection Algorithm

#### If you want to learn about how the motion detection was implemented, here's some more details

1. Weighting the average of the previous frames to form a "background"

2. Subtract the current frame from the weighted average to obain the "difference"

3. Use thresholding on the difference to highlight areas with high difference into a binarized image

4. Use erosions and dilations to clean up the noise from the threshold

5. Use contour detection to grab the contours representing the areas of motion detection
6. Draw a bounding box around the detected motion contour (currently only supporting one bounding box for all movement, will soon implement different boxes for smaller motion)
7. Alert the user through the Twitter API that motion has been detected

  

## More on the Face Detection
I'm currently using OpenCV's deep neural network (dnn) module to detect faces in frames. OpenCV's face detector is based off the [Single Shot Detector (SSD)](https://research.google/pubs/pub44872/)  framework, coupled with a [ResNet base network](https://en.wikipedia.org/wiki/Residual_neural_network)

I'd like to try out the [Multi-task Cascade CNN (MTCNN)](https://arxiv.org/abs/1604.02878) through the [MTCNN library](https://github.com/ipazc/mtcnn) to see if it can yield any performance improvements


I'm also working on implementing a feature to remember faces through facial measurements extraction (the whole pipeline: face detection -> landmark estimation -> measurements extraction) so that the same faces aren't constantly saved within the timespan of milliseconds.