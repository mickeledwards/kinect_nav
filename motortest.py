#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

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
servoMax = 550  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  pulseLength /= 4096                     # 12 bits of resolution
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

def motorcheck():
    for pwm in range(0, 4):
        for servonum in range(0, 16):
            eval('pwm%d' % pwm).setPWM(servonum, 0, servoMax)
            time.sleep(0.25)
            eval('pwm%d' % pwm).setPWM(servonum, 0, servoMin)
            time.sleep(0.25)
            print "Servo %d now!" % (servonum)
    return

def motormove(row,col,dist,servoMin,servoMax):
	pwmsect = 0
	# Turn rows into PWM board
	if row < 2:
		pwmsect = 3
	elif row < 3:
		pwmsect = 2
	elif row < 6:
		pwmsect = 1
	elif row < 8 :
		pwmsect = 0
	# If the row is even, that means it's on the second line of the PWM. Have the col reflect that
	if row % 2 == 0:
		col += 8
	# Use the minimum, maxiumum and gathered distance to find out how far to move servo
	servodist = servoMin + (dist * ((servoMax - servoMin)/7))
	# Move servo
	eval('pwm%d' % pwmsect).setPWM(col, 0, servodist)
        return

motorcheck()

while (True):

    row = input("Please enter a row: ")
    col = input("Please enter a column: ")
    dist = input("Please enter a number 0-7: ")
    motormove(row,col,dist,servoMin,servoMax)
