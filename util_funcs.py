import cv2
import numpy as np

# return 0 for aligned, 1 for turn left, 2 for turn right
def check_align_state(frame, frame_centerX, frame_centerY, contour, margin):
    
    contX,contY,contW,contH = cv2.boundingRect(contour)
            
    cont_centerX = contX + int(contW / 2)
    cont_centerY = contY + int(contH / 2)
    
    # draw blue dot on center of contour (for debugging only)
    cv2.circle(frame,(cont_centerX, cont_centerY),5,(255,0,0),-1)
    
    # draw red dot on center of frame (for debugging only)
    cv2.circle(frame, (frame_centerX, frame_centerY),5,(0,0,255),-1)
    
    offset = frame_centerX - cont_centerX
    
    if (offset > margin):
        return 1
    
    elif (offset < -margin):
        return 2
    
    elif (abs(offset) <= margin):
        return 0