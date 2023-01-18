import cv2
import numpy as np
import time

"""
from picamera.array import PiRGBArray
from picamera import PiCamera
"""
camera_capture = None
cam_on = False



def start_camera():
    print("camera start")
    global cam_on,camera_capture
    cam_on = True
    line_tracking()

def stop_camera():
    print("camera stop")
    global cam_on
    cam_on = False


def line_tracking():
    camera_capture = cv2.VideoCapture(0) #set camera number here
    camera_capture.set(3, 320) #320x240p camera resolution
    camera_capture.set(4, 240)
    while cam_on == True:

        ret,frame = camera_capture.read()
        # 120,120,250 - 50,50,40 for bluelines
        low_black = np.uint8([150,150,150]) #low black and high black values for the camera
        high_black = np.uint8([50,50,0])
        mask = cv2.inRange(frame,high_black,low_black)

        contours, hierarchy = cv2.findContours(mask,1,cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            cmax = max(contours,key = cv2.contourArea)
            M = cv2.moments(cmax)
            if M["m00"]!=0:
                cX = int(M["m10"] / M["m00"]) # X coordinate for the center (320-0)
                cY = int(M["m01"] / M["m00"]) # Y coordinate for the center (240-0)
                #print("cX = %d and cY = %d",cX,cY)
                #cX and cY can be used to give values to the motors/servos
            cv2.drawContours(frame,cmax, -1 , (0,255,0) , 1)
        #for showing the video feed on the monitor
        cv2.imshow("Mask",mask) # black and white mask for the camera frame
        cv2.imshow("Frame",frame) #for showing camera on software
        if cv2.waitKey(10) & 0xff == ord('q'): #kill key " q "
            break    
    camera_capture.release() #destroy opened camera window
    cv2.destroyAllWindows()

