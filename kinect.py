# Imports etc
import freenect
import cv2
import numpy as np
from Adafruit_PWM_Servo_Driver import PWM
import time

# Initialise the PWM device using the default address
pwm = PWM(0x40)
servoMin = 150  # Min pulse length out of 4096
servoMax = 500  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

def nothing(x):
    pass
    
def RegionCheck(foo, ListPath):#foo defines x-coordinate of point

    if (foo <= 130) and (ListPath[0] is not 0):
        ListPath[0] = 0
    if (foo > 130) and (foo <= 320) and (ListPath[1] is not 0):
        ListPath[1] = 0
    if (foo > 320) and (foo <= 510) and (ListPath[2] is not 0):
        ListPath[2] = 0
    if (foo > 510) and (ListPath[3] is not 0):
        ListPath[3] = 0

    return ListPath

#cv2.namedWindow('edge')
cv2.namedWindow('Video')
cv2.moveWindow('Video',5,5)
#cv2.namedWindow('Fin')
#cv2.namedWindow('Win')
kernel = np.ones((5, 5), np.uint8)


print('Press \'b\' in window to stop')
cv2.createTrackbar('val1', 'Video', 37, 1000, nothing)
cv2.createTrackbar('val2', 'Video', 43, 1000, nothing)
cv2.createTrackbar('bin', 'Video',20,50,nothing)
cv2.createTrackbar('erode', 'Video',4,10,nothing)#after plenty of testing
#cv2.createTrackbar('dilate', 'edge',0,10,nothing)
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

while 1:
	distanceint=0

	#get kinect input__________________________________________________________________________
	dst = pretty_depth(freenect.sync_get_depth()[0])#input from kinect
    	#orig = freenect.sync_get_video()[0]
    	#orig = cv2.cvtColor(orig,cv2.COLOR_BGR2RGB) #to get RGB image, which we don't want
	#cv2.flip(orig, 0, orig)#since we keep kinect upside-down
    	#cv2.flip(orig, 1,orig)# thus correcting upside-down mirror effect
    	#cv2.flip(dst, 0, dst)#since we keep kinect upside-down
	cv2.flip(dst, 1,dst)# thus correcting upside-down mirror effect
    
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
	#cv2.createTrackbar('spacing', 'Video', 65, 100, nothing)#for approxPolyDP
    	spac=65 
    	(rows,cols)=dst.shape # 480 rows and 640 cols
    	#print cols

	incrx=0
	incry=0
	distlist = []

    	for i in range(8): #note the presence of colon
		for j in range(8):
			#cv2.circle(dst, (spac*j,spac*i), 1, (0, 255, 0), 1)
			
			if (dst[spac*i,spac*j]==80):
				cv2.putText(dst,"0",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				distlist.append(7)
			elif (dst[spac*i,spac*j]==100):
				cv2.putText(dst,"1",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				distlist.append(6)
			elif (dst[spac*i,spac*j]==120):
                		cv2.putText(dst,"2",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
                		distlist.append(5)
			elif (dst[spac*i,spac*j]==140):
				cv2.putText(dst,"3",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				distlist.append(4)
			elif (dst[spac*i,spac*j]==160):
				cv2.putText(dst,"4",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				distlist.append(3)
			elif (dst[spac*i,spac*j]==180):
				cv2.putText(dst,"5",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				distlist.append(2)
			elif (dst[spac*i,spac*j]==200):
				cv2.putText(dst,"6",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				distlist.append(1)
			elif (dst[spac*i,spac*j]==220):
				cv2.putText(dst,"7",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				distlist.append(0)
                        else:
                                distlist.append(0)
			#print distlist
			
			#incry=incry+1
			#print '\n'
		#incrx=incrx+1
                print distlist
                print '\n'
		distlist = []
        				
	#imshow outputs______________________________________________________________________   
    #cv2.imshow('Input',orig)
	#print flag
	#cv2.destroyWindow('Navig')
	#cv2.line(dst,(130,0),(130,480),(0),1)
	#cv2.line(dst,(320,0),(320,480),(0),1)
	#cv2.line(dst,(510,0),(510,480),(0),1)
    	cv2.imshow('Video', dst)
    	
       	if(cv2.waitKey(1) & 0xFF == ord('b')):
        	break



#Servo Movements______________________________________________________________________   
# while (True):
#   # Change speed of continuous servo on channel O
#   pwm.setPWM(0, 0, servoMin)
#   pwm.setPWM(1, 0, servoMin)
#   pwm.setPWM(2, 0, servoMin)
#   pwm.setPWM(3, 0, servoMin)
#   pwm.setPWM(4, 0, servoMin)
#   pwm.setPWM(5, 0, servoMin)
#   pwm.setPWM(6, 0, servoMin)
#   pwm.setPWM(7, 0, servoMin)
#   time.sleep(1)
#   pwm.setPWM(0, 0, servoMax)
#   pwm.setPWM(1, 0, servoMax)
#   pwm.setPWM(2, 0, servoMax)
#   pwm.setPWM(3, 0, servoMax)
#   pwm.setPWM(4, 0, servoMax)
#   pwm.setPWM(5, 0, servoMax)
#   pwm.setPWM(6, 0, servoMax)
#   pwm.setPWM(7, 0, servoMax)
#   time.sleep(1)
#   pwm.setPWM(8, 0, servoMin)
#   pwm.setPWM(9, 0, servoMin)
#   pwm.setPWM(10, 0, servoMin)
#   pwm.setPWM(11, 0, servoMin)
#   pwm.setPWM(12, 0, servoMin)
#   pwm.setPWM(13, 0, servoMin)
#   pwm.setPWM(14, 0, servoMin)
#   pwm.setPWM(15, 0, servoMin)
#   time.sleep(1)
#   pwm.setPWM(8, 0, servoMax)
#   pwm.setPWM(9, 0, servoMax)
#   pwm.setPWM(10, 0, servoMax)
#   pwm.setPWM(11, 0, servoMax)
#   pwm.setPWM(12, 0, servoMax)
#   pwm.setPWM(13, 0, servoMax)
#   pwm.setPWM(14, 0, servoMax)
#   pwm.setPWM(15, 0, servoMax)
#   time.sleep(1)
#   pwm2.setPWM(0, 1, servoMin)
#   pwm2.setPWM(1, 1, servoMin)
#   pwm2.setPWM(2, 1, servoMin)
#   pwm2.setPWM(3, 1, servoMin)
#   pwm2.setPWM(4, 1, servoMin)
#   pwm2.setPWM(5, 1, servoMin)
#   pwm2.setPWM(6, 1, servoMin)
#   pwm2.setPWM(7, 1, servoMin)
#   time.sleep(1)
#   pwm2.setPWM(0, 1, servoMax)
#   pwm2.setPWM(1, 1, servoMax)
#   pwm2.setPWM(2, 1, servoMax)
#   pwm2.setPWM(3, 1, servoMax)
#   pwm2.setPWM(4, 1, servoMax)
#   pwm2.setPWM(5, 1, servoMax)
#   pwm2.setPWM(6, 1, servoMax)
#   pwm2.setPWM(7, 1, servoMax)
#   time.sleep(1)
#   pwm2.setPWM(8, 1, servoMin)
#   pwm2.setPWM(9, 1, servoMin)
#   pwm2.setPWM(10, 1, servoMin)
#   pwm2.setPWM(11, 1, servoMin)
#   pwm2.setPWM(12, 1, servoMin)
#   pwm2.setPWM(13, 1, servoMin)
#   pwm2.setPWM(14, 1, servoMin)
#   pwm2.setPWM(15, 1, servoMin)
#   time.sleep(1)
#   pwm2.setPWM(8, 1, servoMax)
#   pwm2.setPWM(9, 1, servoMax)
#   pwm2.setPWM(10, 1, servoMax)
#   pwm2.setPWM(11, 1, servoMax)
#   pwm2.setPWM(12, 1, servoMax)
#   pwm2.setPWM(13, 1, servoMax)
#   pwm2.setPWM(14, 1, servoMax)
#   pwm2.setPWM(15, 1, servoMax)
#   time.sleep(1)