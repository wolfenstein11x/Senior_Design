# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 10:24:32 2020

@author: Richard Cheng
MakeBlock Robot Vision Recognition: Deterministic Method
"""
import sys
sys.path.append('/home/pi/Project')

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2 ## Opencv library
import numpy as np
import gpiozero  ## Need to change import MegaPi library instead of gpiozero
from time import sleep
import robot_move_definitions as defs

camera = PiCamera()
image_width = 640
image_height = 480
camera.resolution = (image_width, image_height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(image_width, image_height))
center_image_x = image_width / 2
center_image_y = image_height / 2
minimum_area = 200
maximum_area = 29350    #yellow ball 43000
fast_area = 20000
##
## Robot Pins, change the following code to MegaPi 
##
robot = gpiozero.Robot(left=(22,27), right=(17,18))
forward_speed = 1.0
turn_speed = 0.8

## 
## Find the HUE value by using color_tester.py
##
HUE_VAL = 25
## Selecting HUE range to find the target color 
## Tunable for different color sensitivity 
lower_color = np.array([HUE_VAL-10,100,100])
upper_color = np.array([HUE_VAL+10, 255, 255])

try:
    sleep(0.1)
    ##  Analyzing Camera Frames
    ##  For each frame, capture the image
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        ## Saving image into an array
        image = frame.array
        ## Transfer RGB image data into HSV format
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        ## Keep the desired HSV color
        color_mask = cv2.inRange(hsv, lower_color, upper_color)
    ## The following code is outdated according to the Opencv Library 
    ##    image2, countours, hierarchy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        ## Draw the contour of the distinguish line
        placeholder_error ,countours, hierarchy = cv2.findContours(color_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        ## Initiate target size and location
        object_area = 0
        object_x = 0
        object_y = 0
    ##  Everytime it detects a contour, the loop will start running
    ##  After comparing all the contour found in each frame, the loop ends and distinguished the final target
        for contour in countours:
    ##      Drawing boxes to approximate the shape of the contour
    ##      Find the area of the contour and the center of the contour
            x, y, width, height = cv2.boundingRect(contour)
            found_area = width * height
            center_x = x + (width / 2)  # x,y is the coordinate of top left rect
            center_y = y + (height / 2)
    ##      Assuming the larger contour is most likely the desired target object
    ##      Discard previous info and update the new contour
            if object_area < found_area:
                object_area = found_area
                object_x = center_x
                object_y = center_y
    ##  Target object is found, saving the object's postion
        if object_area > 0:
            ball_location = [object_area, object_x, object_y]
    ##  No contour is found
        else:
            ball_location = None

    ##  React to the ball    
    ##  If a target object is found
        if ball_location:
    ##      Check if the size of the ball is in the requirement
            if (ball_location[0] > minimum_area) and (ball_location[0] < maximum_area):
    ##          May change the boundry to find the ball
                if (ball_location[1] > (center_image_x + (image_width/5))) and (ball_location[0] < fast_area): #divide 12 for ball
    ##                robot.right(turn_speed)
    ##              Tell MegaPi to turn right
                    print('going right fast')
                    cmd = 'right_fast'
                    defs.turn_right_fast()
                elif ball_location[1] < (center_image_x - (image_width/5)) and (ball_location[0] < fast_area): #divide 12 for ball
    ##                robot.left(turn_speed)
    ##              Tell MegaPi to turn right 
                    cmd = 'left_fast'
                    print('going left fast')
                    defs.turn_left_fast()
                elif (ball_location[1] > (center_image_x + (image_width/50))) and (ball_location[0] > fast_area): #divide 12 for ball
    ##                robot.right(turn_speed)
    ##              Tell MegaPi to turn right
                    print('going right')
                    cmd = 'right'
                    defs.turn_right()
                elif ball_location[1] < (center_image_x - (image_width/50)) and (ball_location[0] > fast_area): #divide 12 for ball
    ##                robot.left(turn_speed)
    ##              Tell MegaPi to turn right 
                    cmd = 'left'
                    print('going left')
                    defs.turn_left()
                else:
    ##                robot.forward(forward_speed)
    ##              Tell MegaPi to move forward
                    cmd = 'forward'
                    defs.move_forward()
            elif (ball_location[0] < minimum_area):
    ##            robot.left(turn_speed)
    ##              Tell MegaPi to turn in some direction to search the target if the object is too small
                cmd = 'search'
                defs.search()
                print("Target isn't large enough, searching")
            else:
    ##            robot.stop()
    ##              Tell MegaPi to stop moving
    ##              Picking up the ball            
                print("Target large enough, stopping")
                print("Start picking up the ball")
                defs.stop_cmd()
                sleep(0.1)
                #cmd = 'lower'
                defs.open_gripper()
                sleep(0.1)
                defs.lower_arm()
                sleep(0.1)
                defs.close_gripper()
                sleep(0.1)
                defs.raise_arm()
                sleep(0.1)
        else:
    ##        robot.left(turn_speed)
    ##      No target found, move in one direction to search for the ball
            print("Target not found, searching")
            cmd = 'search'
            defs.search()

        cv2.imshow("Color Mask", color_mask) #69420 blaze it
        cv2.imshow("Image", image)
        cv2.waitKey(1)
        rawCapture.truncate(0)

finally:
    defs.stop_cmd()
    defs.raise_arm()
    defs.open_gripper()
    defs.stop_cmd()

