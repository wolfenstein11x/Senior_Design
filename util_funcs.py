import cv2
import numpy as np

#######################################################################
# Utility functions to help with various tasks, such as aligning with #
# object, and determining which direction to turn                     #
#                                                                     #
#######################################################################

def check_turn_direction(frame, frame_centerX, contour, dead_end_margin):
    
    # get coordinates of contour
    contX,contY,contW,contH = cv2.boundingRect(contour)
    
    # get mid X coordinate of contour
    cont_centerX = contX + int(contW / 2)
    #print("cont_centerX:")
    #print(cont_centerX)
    
    # return 1 for turn right, zero for turn left, or 2 for 180 degree turn
    if (cont_centerX <= frame_centerX):
        
        # check if you are at a dead end or lane line
        if ((frame_centerX - cont_centerX) >= dead_end_margin):
            return 1
        
        # difference is within dead end margin, so robot is at a dead end
        else:
            return 2
    
    elif (cont_centerX >= frame_centerX):
        
        # check if you are at a dead end or lane line
        if ((cont_centerX - frame_centerX) >= dead_end_margin):
            return 0
    
        # difference is within dead end margin, so robot is at a dead end
        else:
            return 2

# return 0 for aligned, 1 for turn left, 2 for turn right
def check_align_state(frame, frame_centerX, contour, margin):
    
    contX,contY,contW,contH = cv2.boundingRect(contour)
            
    cont_centerX = contX + int(contW / 2)
    cont_centerY = contY + int(contH / 2)
    
    # draw blue dot on center of contour (for debugging only)
    #cv2.circle(frame,(cont_centerX, cont_centerY),5,(255,0,0),-1)
    
    # draw red dot on center of frame (for debugging only)
    #cv2.circle(frame, (frame_centerX, frame_centerY),5,(0,0,255),-1)
    
    offset = frame_centerX - cont_centerX
    
    if (offset > margin):
        return 1
    
    elif (offset < -margin):
        return 2
    
    elif (abs(offset) <= margin):
        return 0