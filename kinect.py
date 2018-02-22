from Adafruit_PWM_Servo_Driver import PWM
import time
import freenect
import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('Video')
cv2.moveWindow('Video',5,5)
cv2.namedWindow('Navig',cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow('Navig',400,100)
cv2.moveWindow('Navig',700,5)
kernel = np.ones((5, 5), np.uint8)


print('Press \'b\' in window to stop')
cv2.createTrackbar('val1', 'Video', 37, 1000, nothing)
cv2.createTrackbar('val2', 'Video', 43, 1000, nothing)
cv2.createTrackbar('bin', 'Video',20,50,nothing)
cv2.createTrackbar('erode', 'Video',4,10,nothing)#after plenty of testing
def pretty_depth(depth):
    np.clip(depth, 0, 2**10 - 1, depth)
    depth >>= 2
    depth = depth.astype(np.uint8)
    return depth

while 1:
	flag120=[1, 1, 1, 1]
	flag140=[1, 1, 1, 1]
	f14=0
	f12=0
	f10=0
	f8=0
#get kinect input__________________________________________________________________________
	dst = pretty_depth(freenect.sync_get_depth()[0])
	cv2.flip(dst, 1,dst)
	   
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

	#finding contours__________________________________________________________________________
    	contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    	cv2.drawContours(dst, contours, -1, (0, 0, 255), -1)
 

	#boundingRect approach_______________________________________________________________________
    	cv2.createTrackbar('epsilon', 'Video', 1, 100, nothing)#for approxPolyDP
    	ep=cv2.getTrackbarPos('epsilon', 'Video') 

	#defined points approach (to check: runtime)________________________________________________
	cv2.createTrackbar('spacing', 'Video', 60, 100, nothing)#for approxPolyDP
    	spac=cv2.getTrackbarPos('spacing', 'Video') 
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


