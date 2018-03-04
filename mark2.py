from __future__ import print_function
import freenect
import cv2
import numpy as np
from functions import *
from servofunctions import *
from Adafruit_PWM_Servo_Driver import PWM
import time

def nothing(x):
    pass


# Initialise the PWM devices
pwm0 = PWM(0x40)
pwm1 = PWM(0x41)
pwm2 = PWM(0x48)
pwm3 = PWM(0x43)

# Set frequency to 60 Hz
pwm0.setPWMFreq(60)
pwm1.setPWMFreq(60)
pwm2.setPWMFreq(60)
pwm3.setPWMFreq(60)

servoMin = 150  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096

#cv2.namedWindow('edge')
cv2.namedWindow('Video')
cv2.moveWindow('Video',5,5)
#cv2.namedWindow('Fin')
#cv2.namedWindow('Win')
kernel = np.ones((5, 5), np.uint8)


print('Press ESC in window to stop')
cv2.createTrackbar('bin', 'Video',20,50,nothing)
cv2.createTrackbar('erode', 'Video',4,10,nothing)#after plenty of testing

#cv2.createTrackbar('dilate', 'edge',0,10,nothing)
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth


while 1:
	flag120=[1, 1, 1, 1]
	f12=0
	f8=0
#get kinect input__________________________________________________________________________
	dst = pretty_depth(freenect.sync_get_depth()[0])#input from kinect
    	#orig = freenect.sync_get_video()[0]
    	#orig = cv2.cvtColor(orig,cv2.COLOR_BGR2RGB) #to get RGB image, which we don't want
	#cv2.flip(orig, 0, orig)#since we keep kinect upside-down
    	#cv2.flip(orig, 1,orig)# thus correcting upside-down mirror effect
	dst = cv2.resize(dst,(int(32), int(32)), interpolation = cv2.INTER_AREA)
	dst = cv2.resize(dst,(int(640), int(480)), interpolation = cv2.INTER_AREA)
        dst = cv2.flip(dst,1)

#rectangular border (improved edge detection + closed contours)___________________________
	#cv2.rectangle(dst,(0,0),(640,480),(40,100,0),2)

#image binning (for distinct edges)________________________________________________________
    	binn=cv2.getTrackbarPos('bin', 'Video')
    	e=cv2.getTrackbarPos('erode', 'Video')
    	#d=cv2.getTrackbarPos('dilate', 'edge')
    	dst = (dst/binn)*binn
    	#dst = (dst/20)*20 #after plenty of testing
    	dst=cv2.erode(dst, kernel, iterations=e)
    	#dst=cv2.dilate(dst, kernel, iterations=d)#dilations don't help


#Video detection___________________________________________________________________________
    	v1 = 37
    	v2 = 43
    	v1 = cv2.getTrackbarPos('val1', 'Video')
    	v2 = cv2.getTrackbarPos('val2', 'Video')
    	edges = cv2.Canny(dst, v1, v2)
    	#cv2.imshow('edge', edges)

#finding contours__________________________________________________________________________
    	contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    	cv2.drawContours(dst, contours, -1, (0, 0, 255), -1)
    #cv2.drawContours(orig, contours, -1, (0, 0, 255), -1)
#finding contour center of mass (moments)___________________________________________________
    	cx=0
    	cy=0
    	try:
        	for i in range(len(contours)):
            		M = cv2.moments(contours[i])

            		cx = int(M['m10']/M['m00'])
            		cy = int(M['m01']/M['m00'])
            		#cv2.circle(dst, (cx, cy), 6, (0, 255, 0), 3)
           # cx = int(cx/len(contours))
           # cy = int(cy/len(contours))
    	except:
      		pass

#boundingRect approach_______________________________________________________________________
    	cv2.createTrackbar('epsilon', 'Video', 1, 100, nothing)#for approxPolyDP
    	ep=cv2.getTrackbarPos('epsilon', 'Video')
    	#for i in range(len(contours)):
		#if (cv2.contourArea(contours[i])>1):
    			#x,y,w,h = cv2.boundingRect(contours[i])#upright rectangle
			#cv2.rectangle(dst,(x,y),(x+w,y+h),(150,100,0),2)
			#cv2.circle(dst, (x+w/2,y+h/2), 1, (0, 255, 0), 3)

			#rect=cv2.minAreaRect(contours[i])#rotated rect
			#box = cv2.cv.BoxPoints(rect)                     Rotated Rect approach failed
			#box = np.int0(box)
			#cv2.drawContours(dst,[box],0,(50,0,255),2)
#approxPolyDP approach________________________________________________________________________
		#approx = cv2.approxPolyDP(contours[i],(ep/100)*cv2.arcLength(contours[i],True),True)
		#cv2.drawContours(dst, approx, -1, (0, 0, 2), 1)

#defined points approach (to check: runtime)________________________________________________
    	spac=60
    	spacj=80
    	rows=480
    	cols=640
    	motornum=0
    	#print cols
	print("\033c")

    	for i in range(0,rows/spac): #note the presence of colon
		for j in range(0, cols/spacj):
			cv2.circle(dst, (spacj*j,spac*i), 1, (0, 255, 0), 1)
			if (dst[spac*i,spac*j]==80):
				cv2.putText(dst,"0",(spacj*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),2)
				motormove(i,j,7,servoMin,servoMax)
			if (dst[spac*i,spac*j]==100):
				cv2.putText(dst,"1",(spacj*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),2)
				motormove(i,j,6,servoMin,servoMax)
			if (dst[spac*i,spac*j]==120):
				cv2.putText(dst,"2",(spacj*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0),1)
				motormove(i,j,5,servoMin,servoMax)
			if (dst[spac*i,spac*j]==140):
				cv2.putText(dst,"3",(spacj*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				motormove(i,j,4,servoMin,servoMax)
			if (dst[spac*i,spac*j]==160):
				cv2.putText(dst,"4",(spacj*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				motormove(i,j,3,servoMin,servoMax)
			if (dst[spac*i,spac*j]==180):
				cv2.putText(dst,"5",(spacj*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				motormove(i,j,2,servoMin,servoMax)
			if (dst[spac*i,spac*j]==200):
				cv2.putText(dst,"6",(spacj*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				motormove(i,j,1,servoMin,servoMax)
			if (dst[spac*i,spac*j]==220):
				cv2.putText(dst,"7",(spacj*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				motormove(i,j,0,servoMin,servoMax)
			print(motornum, end='')
		print ('\n')



#imshow outputs______________________________________________________________________
    #cv2.imshow('Input',orig)
	#print flag

	cv2.line(dst,(80,0),(80,480),(0),1)
	cv2.line(dst,(160,0),(160,480),(0),1)
	cv2.line(dst,(240,0),(240,480),(0),1)
	cv2.line(dst,(320,0),(320,480),(0),1)
	cv2.line(dst,(400,0),(400,480),(0),1)
	cv2.line(dst,(480,0),(480,480),(0),1)
	cv2.line(dst,(560,0),(560,480),(0),1)

	cv2.line(dst,(0,60),(640,60),(0),1)
	cv2.line(dst,(0,120),(640,120),(0),1)
	cv2.line(dst,(0,180),(640,180),(0),1)
	cv2.line(dst,(0,240),(640,240),(0),1)
	cv2.line(dst,(0,300),(640,300),(0),1)
	cv2.line(dst,(0,360),(640,360),(0),1)
	cv2.line(dst,(0,420),(640,420),(0),1)

    	cv2.imshow('Video', dst)

       	if(cv2.waitKey(1) & 0xFF == ord('b')):
        	break
