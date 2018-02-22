
from Adafruit_PWM_Servo_Driver import PWM
import time
import freenect
import cv2
import numpy as np

##DEFINE FUNCTIONS##
def nothing(x):
    pass

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  pulseLength /= 4096                     # 12 bits of resolution
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)
	
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

def motormove(row,col,dist,servoMin,servoMax):
	
	# Turn rows into PWM board
	if row < 2:
		pwmsect = 0
	elif row < 4:
		pwmsect = 1
	elif row < 6:
		pwmsect = 2
	else:
		pwmsect = 3
		
	# If the row is even, that means it's on the second line of the PWM. Have the col reflect that
	if row % 2 == 0:
		col += 8
		
	# Use the minimum, maxiumum and gathered distance to find out how far to move servo
	servodist = servoMin + (dist * ((servoMax - servoMin)/7))
	
	# Move servo
	eval('pwm%d' % pwmsect).setPWM(col, 0, servodist)
	return

def motorcheck():
    for pwm in range(0, 3):
        for servonum in range(0, 16):
            eval('pwm%d' % pwm).setPWM(servonum, 0, servoMin)
            time.sleep(0.25)
          #  eval('pwm%d' % pwm).setPWM(servonum, 0, servoMax)
            time.sleep(0.25)
            print "Servo %d now!" % (servonum)
	return

##END FUNCTIONS##

cv2.namedWindow('Video')
cv2.moveWindow('Video',5,5)
kernel = np.ones((5, 5), np.uint8)


#print('Press \'b\' in window to stop')
cv2.createTrackbar('val1', 'Video', 37, 1000, nothing)
cv2.createTrackbar('val2', 'Video', 43, 1000, nothing)
cv2.createTrackbar('bin', 'Video',20,50,nothing)
cv2.createTrackbar('erode', 'Video',4,10,nothing)#after plenty of testing
cv2.createTrackbar('dilate', 'edge',0,10,nothing)


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


while 1:
	#get kinect input__________________________________________________________________________
	dst = pretty_depth(freenect.sync_get_depth()[0])
	cv2.flip(dst, 1,dst)
    
	#rectangular border (improved edge detection + closed contours)___________________________ 
	cv2.rectangle(dst,(0,0),(640,480),(40,100,0),2)
	   
	#image binning (for distinct edges)________________________________________________________
	binn=cv2.getTrackbarPos('bin', 'Video') 
	e=cv2.getTrackbarPos('erode', 'Video') 
	d=cv2.getTrackbarPos('dilate', 'edge') 
	dst = (dst/binn)*binn
	#dst = (dst/20)*20 #after plenty of testing 
	dst=cv2.erode(dst, kernel, iterations=e)
	dst=cv2.dilate(dst, kernel, iterations=d)#dilations don't help

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

	#defined points approach (to check: runtime)________________________________________________
	cv2.createTrackbar('spacing', 'Video', 40, 100, nothing)#for approxPolyDP
    spac=cv2.getTrackbarPos('spacing', 'Video') 
    (rows,cols)=dst.shape # 480 rows and 640 cols
    
	#print("\033c")
    #print cols
	xnum = 0
	motorarray = [[0,0,0,0,0,0,0,0]
				  [0,0,0,0,0,0,0,0]
				  [0,0,0,0,0,0,0,0]
				  [0,0,0,0,0,0,0,0]
				  [0,0,0,0,0,0,0,0]
				  [0,0,0,0,0,0,0,0]
				  [0,0,0,0,0,0,0,0]
				  [0,0,0,0,0,0,0,0]]
	
	#init Y loop
	for i in range(0,8):
		#init X Loop
		for j in range(cols/spac):
			if (dst[spac*i,spac*j]>=80):
				cv2.putText(dst,"0",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				newnum = 7
			elif (dst[spac*i,spac*j]==100):
				cv2.putText(dst,"1",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				newnum = 6
			elif (dst[spac*i,spac*j]==120):
				cv2.putText(dst,"2",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				newnum = 5
			elif (dst[spac*i,spac*j]==140):
				cv2.putText(dst,"3",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				newnum = 4
			elif (dst[spac*i,spac*j]==160):
				cv2.putText(dst,"4",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				newnum = 3
			elif (dst[spac*i,spac*j]==180):
				cv2.putText(dst,"5",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				newnum = 2
			elif (dst[spac*i,spac*j]==200):
				cv2.putText(dst,"6",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				newnum = 1
			else:
				cv2.putText(dst,"7",(spac*j,spac*i),cv2.FONT_HERSHEY_PLAIN,1,(0,200,20),1)
				newnum = 0
				
				#If the X number is even (0,2,4,6,8,10,12,14), move the current value to the old number spot and wipe new number
			if j % 2 == 0:
				oldnum = newnum
				newnum = 0	
				
				#If the x number is odd (1,3,5,7,9,11,13,15), average the even and odd measurement to make a total of 8 x measurements
			if j % 2 != 0:
				motorarray[xnum][i] = round((newnum+oldnum)/2)
				newnum = 0
				oldnum = 0
				xnum = xnum + 1
				
				
				
			print i,j
		print '\n'
		

		#imshow outputs______________________________________________________________________   
		cv2.imshow('Video', dst)
		if(cv2.waitKey(1) & 0xFF == ord('b')):
			break
