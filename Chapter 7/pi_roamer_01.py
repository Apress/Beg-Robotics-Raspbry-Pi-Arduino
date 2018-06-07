import serial
import time
import random

from Adafruit_MotorHAT import Adafruit_MotorHAT as amhat
from Adafruit_MotorHAT import Adafruit_DCMotor as adamo

# create motor objects
motHAT = amhat(addr=0x60)
mot1 = motHAT.getMotor(1)
mot2 = motHAT.getMotor(2)
mot3 = motHAT.getMotor(3)
mot4 = motHAT.getMotor(4)

# open serial port
ser = serial.Serial('/dev/ttyACM0', 115200)

# create variables
# sensors
distMid = 0.0
distLeft = 0.0
distRight = 0.0

# motor multipliers
m1Mult = 1.0
m2Mult = 1.0
m3Mult = 1.0
m4Mult = 1.0

# distance threshold
distThresh = 12.0
distCutOff = 30.0

# speeds
speedDef = 200
leftSpeed = speedDef
rightSpeed = speedDef
speedMod = 20
turnTime = 1.0
defTime = 0.01
driveTime = defTime

def driveMotors(leftChnl = speedDef, rightChnl = speedDef,
                duration = defTime):
    # determine the speed of each motor by multiplying
    # the channel by the motors multiplier
    m1Speed = leftChnl * m1Mult
    m2Speed = leftChnl * m2Mult
    m3Speed = rightChnl * m3Mult
    m4Speed = rightChnl * m4Mult

    # set each motor speed. Since the speed can be a
    # negative number, we take the absolute value
    mot1.setSpeed(abs(int(m1Speed)))
    mot2.setSpeed(abs(int(m2Speed)))
    mot3.setSpeed(abs(int(m3Speed)))
    mot4.setSpeed(abs(int(m4Speed)))

    # run the motors. if the channel is negative, run
    # reverse. else run forward
    if(leftChnl < 0):
        mot1.run(amhat.BACKWARD)
        mot2.run(amhat.BACKWARD)
    else:
        mot1.run(amhat.FORWARD)
        mot2.run(amhat.FORWARD)

    if (rightChnl > 0):
        mot3.run(amhat.BACKWARD)
        mot4.run(amhat.BACKWARD)
    else:
        mot3.run(amhat.FORWARD)
        mot4.run(amhat.FORWARD)

    # wait for duration
    time.sleep(duration)

try:
    while 1:
        # read the serial port
        val = ser.readline().decode('utf=8')
        print val

        # parse the serial string
        parsed = val.split(',')
        parsed = [x.rstrip() for x in parsed]

        if(len(parsed)>2):
            distMid = float(parsed[0] + str(0))
            distLeft = float(parsed[1] + str(0))
            distRight = float(parsed[2] + str(0))

        # apply cutoff distance
        if(distMid > distCutOff):
            distMid = distCutOff
        if(distLeft > distCutOff):
            distLeft = distCutOff
        if(distRight > distCutOff):
            distRight = distCutOff

        # reset driveTime
        driveTime = defTime
        
        # if obstacle to left, steer right by increasing
        # leftSpeed and running rightSpeed negative defSpeed
        # if obstacle to right, steer to left by increasing
        # rightSpeed and running leftSpeed negative
        if(distLeft <= distThresh):
            leftSpeed = speedDef
            rightSpeed = -speedDef
        elif (distRight <= distThresh):
            leftSpeed = -speedDef
            rightSpeed = speedDef
        else:
            leftSpeed = speedDef
            rightSpeed = speedDef

        # if obstacle dead ahead, stop then turn toward most
        # open direction. if both directions open, turn random
        if(distMid <= distThresh):
            # stop
            leftSpeed = 0
            rightSpeed = 0
            driveMotors(leftSpeed, rightSpeed, 1)
            time.sleep(1)
            leftSpeed = -150
            rightSpeed = -150
            driveMotors(leftSpeed, rightSpeed, 1)
            # determine preferred direction. if distLeft >
            # distRight, turn left. if distRight > distLeft,
            # turn right. if equal, turn random
            dirPref = distRight - distLeft
            if(dirPref == 0):
                dirPref = random.random()
            if(dirPref < 0):
                leftSpeed = -speedDef
                rightSpeed = speedDef
            elif(dirPref > 0):
                leftSpeed = speedDef
                rightSpeed = -speedDef
            driveTime = turnTime

        # drive the motors
        driveMotors(leftSpeed, rightSpeed, driveTime)

        ser.flushInput()

except KeyboardInterrupt:
    mot1.run(amhat.RELEASE)
    mot2.run(amhat.RELEASE)
    mot3.run(amhat.RELEASE)
    mot4.run(amhat.RELEASE)
