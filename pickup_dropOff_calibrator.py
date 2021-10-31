#! /usr/bin/python3

##############################################################################
# Position the block so that it is in range to be picked up by the robot,    #
# or position the robot so it is in range to drop off in the container.      #
# Then observe the contour size                                              #
##############################################################################

import cv2
import numpy as np
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera

block_area = 0
container_area = 0


# yellow mask limits
lower_yellow = np.array([15,100,100])
upper_yellow = np.array([35,255,255])

# green mask limits
lower_green = np.array([36,0,0])
upper_green = np.array([86,255,255])

# initialize camera and grab a reference to the raw camera capture
camera = PiCamera()
image_width = 640
image_height = 480
camera.resolution = (image_width, image_height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(image_width, image_height))

# allow the camera time to warmup
sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image - this array
    # will be 3D, representing the width, height, and # of channels
    image = frame.array
        
    # convert image from BGR format to HSV format
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
    # create mask for yellow blocks
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # create a mask for green container
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # do erosion to get rid of white spots
    kernel = np.ones((5,5),dtype=np.uint8)
    blocks = cv2.erode(yellow_mask,kernel,iterations=4)
    container = cv2.erode(green_mask,kernel,iterations=4)
    
    # find contour of block
    yellow_contours, heir = cv2.findContours(blocks, cv2.RETR_CCOMP,
                                             cv2.CHAIN_APPROX_SIMPLE)
    
    # find contours of container
    green_contours, heir = cv2.findContours(container, cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)
    
    
    # find biggest yellow contour
    for cont in yellow_contours:
        yellow_area = cv2.contourArea(cont)
    
        if (yellow_area > block_area):
            block_area = yellow_area
            
    #print(block_area)
    
    # find biggest green contour
    for cont in green_contours:
        green_area = cv2.contourArea(cont)
        
        if (green_area > container_area):
            container_area = green_area
    
    print(container_area)
    
    # show the frame (for debugging purposes)
    masked_video = blocks
    cv2.imshow("Masked Video", masked_video)
    key = cv2.waitKey(1) & 0xFF
        
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
       
    # if the 'q' key is pressed, break from the loop
    if key == ord('q'):
        break