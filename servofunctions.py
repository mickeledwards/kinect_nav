def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  pulseLength /= 4096                     # 12 bits of resolution
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)


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
