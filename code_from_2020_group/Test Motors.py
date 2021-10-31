#! /usr/bin/python3

from megapi import *
from time import sleep

#PORT = 3


bot = MegaPi()
bot.start()                 #use this for direct connection to raspberry pi
#bot.start('/dev/ttyUSB0')   #use this if using the USB port to connect to the floating megapi



for PORT in range(1,5):                #cycles through motors and runs them forward and back
    bot.encoderMotorRun(PORT,30)
    print('running', PORT)
    sleep(1)
    bot.encoderMotorRun(PORT,0)
    print('stop')
    sleep(0.5)
    bot.encoderMotorRun(PORT,-30)
    print('running', PORT, 'back')
    sleep(1)
    bot.encoderMotorRun(PORT,0)
    print('stop')






# bot.motorRun(4, 30)
# sleep(0.5)
# bot.motorRun(4, -30)
# sleep(0.5)
# bot.motorRun(4,0)



#bot.move_forward()
#print("moving forward")
#sleep(2)

#bot.stop_cmd()
#print("end of test")

