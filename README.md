# securityCam
🎥 A real-time camera streaming application with motion detection alerts

## What is it?
securityCam is a real-time security camera application built on a **flask** server to stream video to the internet. Motion detection was implemented using **OpenCV** to issue alerts when motion is detected.


## More on the Motion Detection Algorithm
#### If you want to learn about how the motion detection was implemented, here's some more details
1. Weighting the average of the previous frames to form a "background"
2. Subtract the current frame from the weighted average to obain the "difference"
3. Use thresholding on the difference to highlight areas with high difference
4. Using erosions and dilations clean up the noise from the threshold
5. Use contour detection to grab the contours representing the areas of motion detection