#! /usr/bin/python3
import cv2
import numpy as np
import motion


# set your mask limits
lower_blue = np.array([90,40,40])
upper_blue = np.array([150,255,255])

# start filming (but not showing it)
cap = cv2.VideoCapture(0)

# 
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# main function
while True:
    
    # move forward until seeing a big enough contour
    motion.move_forward(1,1)
    
    # frame is the picture
    ret,frame = cap.read()
    
    # convert image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   
    # create mask
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # do erosion to get rid of white spots
    kernel = np.ones((5,5),dtype=np.uint8)
    eroded = cv2.erode(mask,kernel,iterations=4)
    
    # edge detection
    #edges = cv2.Canny(image=eroded,threshold1=127,
    #                 threshold2=127)
    
    contours, heir = cv2.findContours(eroded, cv2.RETR_CCOMP,
                                   cv2.CHAIN_APPROX_SIMPLE)
    
    # draw all contours on original image
    for i in range(len(contours)):
        cv2.drawContours(frame, contours, i, [0,255,0], 3)
    
    # get the center point of each lane
    for cont in contours:
        #M = cv2.moments(cont)
        #cX = int(M["m10"] / (M["m00"] + 0.0000001))
        #cY = int(M["m01"] / (M["m00"] + 0.0000001))
        area = cv2.contourArea(cont)
        if (area > 25000):
            motion.stop()
            motion.backupAndRotate()
            #print("Contour area: ", area)
        #else:
            #motion.move_forward(1,1)
        #print(area)
        # draw red circle at center points
        #cv2.circle(frame, (cX,cY), 3, (0,0,255), -1)
        
    
    # show the camera
#    cv2.imshow('lanes', frame)
    
    
    # exit loop if user presses 'q'
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break




# stop filming
#cap.release()

#cv2.destroyAllWindows()

print("exiting program")
