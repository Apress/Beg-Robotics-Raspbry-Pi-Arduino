
from Adafruit_MotorHAT import Adafruit_MotorHAT as amhat, Adafruit_DCMotor as adcm

import time

# create 2 motor objects
mh = amhat(addr=0x60)

motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)

motor3 = mh.getMotor(3)
motor4 = mh.getMotor(4)

# set start speed
motor1.setSpeed(0)
motor2.setSpeed(0)

motor3.setSpeed(0)
motor4.setSpeed(0)

# direction variable
direction = 0

# wrap actions in try loop
try:
    while True:
        # if direction = 1 then motor1 forward and motor2 backward
        # else motor1 backward and motor2 forward
        if direction == 0:
            motor1.run(amhat.FORWARD)
            motor2.run(amhat.FORWARD)
            motor3.run(amhat.FORWARD)
            motor4.run(amhat.FORWARD)
        else:
            motor1.run(amhat.BACKWARD)
            motor2.run(amhat.BACKWARD)
            motor3.run(amhat.BACKWARD)
            motor4.run(amhat.BACKWARD)

        # ramp up the speed from 50 to 255 
        for i in range(50,255):
 
            motor1.setSpeed(i)
            motor2.setSpeed(i)
            motor3.setSpeed(i)
            motor4.setSpeed(i)

            #time.sleep(0.01)

        # ramp down the speed from 255 to 50
        for i in reversed(range(50,255)):

            motor1.setSpeed(i)
            motor2.setSpeed(i)
            motor3.setSpeed(i)
            motor4.setSpeed(i)

            #time.sleep(0.01)

        # wait half a second
        time.sleep(0.5)

        # change directions
        if direction == 0:
            direction = 1
        else:
            direction = 0

# kill motors and exit program on ctrl-c
except KeyboardInterrupt:
    motor1.run(amhat.RELEASE)
    motor2.run(amhat.RELEASE)
    motor3.run(amhat.RELEASE)
    motor4.run(amhat.RELEASE)
