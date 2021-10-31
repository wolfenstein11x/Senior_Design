#! /usr/bin/python3

##########################################################################################
# This is the code used for the video demonstration. Feel free to contact me with any    #
# any questions at c.wolfe132@gmail.com                                                  #
#                                                                                        #
##########################################################################################


import cv2
import numpy as np
import motion
import util_funcs as util
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera

# constants
BLOCK_AREA = 300
PICKUP_AREA = 20000
BOUNDARY_AREA = 12000
CONTAINER_AREA = 40000
DROP_OFF_AREA = 120000
ALIGN_MARGIN = 25
DEAD_END_MARGIN = 10


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

# get center of frame
frame_centerX = int(image_width / 2)
frame_centerY = int(image_height / 2)


try:
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
        
        # reset observed contours
        block_area = 0
        boundary_area = 0
        container_area = 0
        
        # reset turn direction and align states
        turn_dir = 0
        align_state = 1
        container_align_state = 1
        
        # find the biggest blue contour
        for cont in blue_contours:
            blue_area = cv2.contourArea(cont)
            
            if (blue_area > boundary_area):
                boundary_area = blue_area
                
                # in case the contour is big enough that the robot must turn,
                # check if the robot should turn left or right
                turn_dir = util.check_turn_direction(boundaries, frame_centerX, cont,
                                                     DEAD_END_MARGIN)        
        #print("boundary area:")
        #print(boundary_area)
                
        # find biggest yellow contour
        for cont in yellow_contours:
            yellow_area = cv2.contourArea(cont)
            
            if (yellow_area > block_area):
                block_area = yellow_area
                
                # in case the contour is big enough that the robot pick up block,
                # check if the robot should align
                align_state = util.check_align_state(blocks, frame_centerX, cont,
                                                     ALIGN_MARGIN)
        #print("block area:")
        #print(block_area)
        
        
        # find biggest green contour
        for cont in green_contours:
            green_area = cv2.contourArea(cont)
            
            if (green_area > container_area):
                container_area = green_area
                
                # in case the contour is big enough that the robot put down block,
                # check if the robot should align
                container_align_state = util.check_align_state(container, frame_centerX,
                                                               cont,ALIGN_MARGIN)
        #print("container area:")
        #print(container_area)
        
        # if contour boundary is bigger than limit, robot is at boundary and must turn 
        if (boundary_area > BOUNDARY_AREA):
            motion.stop()
            sleep(0.5)
            
            # check turn direction, then backup and turn
            if (turn_dir == 1):
                motion.move_backward(0.5)
                sleep(0.5)
                motion.turn_right(10)
                sleep(0.5)
            elif (turn_dir == 0):
                motion.move_backward(0.5)
                sleep(0.5)
                motion.turn_left(10)
                sleep(0.5)
            elif (turn_dir == 2):
                motion.turn_left(60)
                sleep(0.5)
                
        
        # if block contour is bigger than limit, align
        elif ((block_area > BLOCK_AREA) and (block_area < PICKUP_AREA)):
            motion.stop()
            sleep(0.1)
            
            if (align_state == 1):
                # block is to the left, so turn slightly left
                motion.turn_left(2)
                
            elif (align_state == 2):
                # block is to the right, so turn slightly right
                motion.turn_right(2)
            
            else:
                # block is aligned, so move forward
                sleep(0.1)
                motion.move_forward(0.2)
                sleep(0.1)
         
        # if block contour is big enough, pick it up
        elif (block_area > PICKUP_AREA):
            sleep(0.1)
            motion.pickup_item()
         
        # if container contour is bigger than limit, align
        elif ((container_area > CONTAINER_AREA) and (container_area < DROP_OFF_AREA)):
            motion.stop()
            sleep(0.5)
            
            if (container_align_state == 1):
                # container is to the left, so turn slightly left
                motion.turn_left(3)
                
            elif (container_align_state == 2):
                # container is to the right, so turn slightly right
                motion.turn_right(3)
            
            else:
                # container is aligned, so move forward
                motion.stop()
                sleep(0.1)
                motion.move_forward(0.2)
                sleep(0.1)
                
                
        # if container contour is big enough, drop off block, back up, and turn around
        elif (container_area > DROP_OFF_AREA):
            sleep(0.5)
            motion.drop_item()
            sleep(0.5)
            motion.move_backward(1)
            sleep(0.5)
            motion.turn_left(60)
                
                
        
        # if no contours bigger than limits, robot can go forward
        else:
            motion.move_forward(0.5)
            
        
        # show the frame (for debugging purposes)
        #masked_video = boundaries #+ blocks + container
        #regular_video = image
        #cv2.imshow("Masked Video", masked_video)
        #cv2.imshow("Regular video", regular_video)
        #key = cv2.waitKey(1) & 0xFF
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
       
                             
        
finally:
    print("\nturning off motors and exiting program")
    cv2.destroyAllWindows()
    motion.stop()














