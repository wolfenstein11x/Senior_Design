#! /usr/bin/python3
import cv2
import numpy as np
import motion

# these values may need to be adjusted
BOUNDARY_AREA = 25000
BLOCK_AREA_MIN = 25000
BLOCK_AREA_MAX = 35000
PLATFORM_AREA = 70000

# bool to keep track of when the robot is carrying a block
holdingBlock = False

# set blue mask limits
lower_blue = np.array([90,40,40])
upper_blue = np.array([150,255,255])

# set yellow mask limits
lower_yellow = np.array([15,100,100])
upper_yellow = np.array([35,255,255])

# start filming (but not showing it)
cap = cv2.VideoCapture(0)

# set dimensions of frames
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# main function
while True:
    
    # move forward until seeing a big enough contour
    motion.move_forward(0,0,0)
    
    # frame is the picture
    ret,frame = cap.read()
    
    # convert image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    # create blue and yellow masks
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # do erosion to get rid of white spots
    kernel = np.ones((5,5),dtype=np.uint8)
    boundaries = cv2.erode(blue_mask,kernel,iterations=4)
    blocks = cv2.erode(yellow_mask,kernel,iterations=4)
    
    # find contours of boundaries
    blue_contours, heir = cv2.findContours(boundaries, cv2.RETR_CCOMP,
                                           cv2.CHAIN_APPROX_SIMPLE)
    # find contours of blocks
    yellow_contours, heir = cv2.findContours(blocks, cv2.RETR_CCOMP,
                                             cv2.CHAIN_APPROX_SIMPLE)
    
    # check if boundary contours are big enough
    for cont in blue_contours:
        area = cv2.contourArea(cont)
        if (area > BOUNDARY_AREA):
            motion.stop()
            motion.backupAndRotate()
    
    # check if any yellow contours are big enough
    for cont in yellow_contours:
        area = cv2.contourArea(cont)
        
        # encounter block platform 
        if (area > PLATFORM_AREA):
            # put block on platform if holding one
            if (holdingBlock == True):
                motion.put_down_item()
                motion.turn_around()
                holdingBlock = False
        
        # encounter block
        elif (area > BLOCK_AREA_MIN and area < BLOCK_AREA_MAX):
            # pick up block if not holding one
            if (holdingBlock == False):
                motion.pickup_item()
                holdingBlock = True
            
            # go around block if holding one
            else:
                pass
                # TODO find a better way to do this
                # the problem is when it sees the platform from far away
                # it mistakes it for a block, and avoids it
                #motion.stop()
                #motion.backupAndRotate()
            
    # show the regular video (for debugging only)
    #cv2.imshow('regular video', frame)
    
    # show the masked video (for debugging only)
    #masked_video = boundaries + blocks
    #cv2.imshow('masked video', masked_video)
    
    
    # stop video if user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




# stop filming and close windows if in debugging mode
#cap.release()
#cv2.destroyAllWindows()

print("exiting program")
