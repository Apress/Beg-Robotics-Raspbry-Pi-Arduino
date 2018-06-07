
from Adafruit_MotorHAT import Adafruit_MotorHAT as amhat, Adafruit_DCMotor as adcm

import time

# create a motor object
mh = amhat(addr=0x60)
myMotor = mh.getMotor(1)

# set start speed
myMotor.setSpeed(150)

try:
    while True:
        # set direction
        myMotor.run(amhat.FORWARD)

        # wait 1 second
        time.sleep(1)

        # stop motor
        myMotor.run(amhat.RELEASE)

        # wait 1 second
        time.sleep(1)

except KeyboardInterrupt:
    myMotor.run(amhat.RELEASE)




