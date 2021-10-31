#! /usr/bin/python3

###########################################################################
# Run this script to make sure the robot is seeing the colors properly    #
# Note that the color of the contours don't match the color of the object #                                          #
# That is done on purpose, so the contours stand out                      #                                                 #
###########################################################################

import cv2
import numpy as np
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera

# blue mask limits
lower_blue = np.array([90,40,40])
upper_blue = np.array([150,255,255])

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
        
    # create a mask for blue boundary
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
    # create a mask for green container
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
    # do erosion to get rid of white spots
    kernel = np.ones((5,5),dtype=np.uint8)
    blocks = cv2.erode(yellow_mask,kernel,iterations=4)
    boundaries = cv2.erode(blue_mask,kernel,iterations=4)
    container = cv2.erode(green_mask,kernel,iterations=4)
    
    # find contours of blocks
    yellow_contours, heir = cv2.findContours(blocks, cv2.RETR_CCOMP,
                                             cv2.CHAIN_APPROX_SIMPLE)
        
    # find contours of boundaries
    blue_contours, heir = cv2.findContours(boundaries, cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)
        
    # find contours of container
    green_contours, heir = cv2.findContours(container, cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)
    
    # draw the contours on blocks, boundaries, and container
    cv2.drawContours(image, yellow_contours, -1, (0,0,255), 3)
    cv2.drawContours(image, blue_contours, -1, (0,255,255), 3)
    cv2.drawContours(image, green_contours, -1, (255,0,0), 3)
    
    # show the frame (for debugging purposes)
    masked_video = blocks + boundaries + container
    #cv2.imshow("Masked Video", masked_video)
    cv2.imshow("Contours", image)
    key = cv2.waitKey(1) & 0xFF
        
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
       
    # if the 'q' key is pressed, break from the loop
    if key == ord('q'):
        break



