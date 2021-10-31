#! /usr/bin/python3
from megapi import *
from time import sleep

bot = MegaPi()
bot.start()

# these numbers will change when we get the new connectors
LF_MOTOR_PORT = 1
RR_MOTOR_PORT = 4
ARM_MOTOR_PORT = 3
CLAW_MOTOR_PORT = 2

#function reference:
############################
#move_forward(time,speed=90)
#move_backward(time,speed=90)
#turn_right(degrees=90)
#turn_left(degrees=90)
#pivot_right(degrees=90)
#pivot_left(degrees=90)
#pickup_item()
#put_down_item()
#drop_item()
#stop()


#updated this to be easier to use, just input the time you want it to move and then you can change the defaults if it is necessary

def move_forward(time, speed=90):
    bot.encoderMotorRun(LF_MOTOR_PORT, -speed)
    bot.encoderMotorRun(RR_MOTOR_PORT, speed)
    sleep(time)
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)
 
def move_backward(time, speed=90):
    bot.encoderMotorRun(LF_MOTOR_PORT, speed)
    bot.encoderMotorRun(RR_MOTOR_PORT, -speed)
    sleep(time)
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)

#turn functions only turn the motor on the outside of the turn, this is the same speed as pivoting, but it doesn't get bogged down
# as much when you are going for more than 45 degrees. This would be the default when driving around the area, not for precise alignment

#just call the function and input your desired degrees to turn and it will be close to your target angle. It won't be perfect,
# but doing multiple smaller adjustmests may be better than trying to get exact on the first pivot/turn

def turn_right(degrees=90):
    #print("turn right ", degrees, " degrees")
    speed=90
    time=7*(degrees/90)
    #bot.encoderMotorRun(LF_MOTOR_PORT, speed)
    bot.encoderMotorRun(RR_MOTOR_PORT, speed)
    sleep(time)
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)
    
def turn_left(degrees=90):
    #print("turn left ", degrees, " degrees")
    speed=90
    time=7*(degrees/90)
    bot.encoderMotorRun(LF_MOTOR_PORT, -speed)
    #bot.encoderMotorRun(RR_MOTOR_PORT, -speed)
    sleep(time)
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)

#pivot functions run both motors so the robot rotates in place, it gets bogged down if you pivot for more than 45 degrees,
# in one go, so ideally it could be used for precise lining up at the target and not for driving around autonomously.

def pivot_right(degrees=90):
    print("pivot right ", degrees, " degrees")
    speed=90
    time=7*(degrees/90)
    bot.encoderMotorRun(LF_MOTOR_PORT, speed)
    bot.encoderMotorRun(RR_MOTOR_PORT, speed)
    sleep(time)
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)
    
def pivot_left(degrees=90):
    print("pivot left ", degrees, " degrees")
    speed=90
    time=7*(degrees/90)
    bot.encoderMotorRun(LF_MOTOR_PORT, -speed)
    bot.encoderMotorRun(RR_MOTOR_PORT, -speed)
    sleep(time)
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)
    
def stop():
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)
    bot.encoderMotorRun(ARM_MOTOR_PORT,0)
    bot.encoderMotorRun(CLAW_MOTOR_PORT,0)
    
def backupAndRotate():
    move_backward(0,0,0)
    turn_left(0,0)
    
    # delay for demonstration purposes only
    sleep(0.5)
    
def raise_claw(speed, time):
    bot.encoderMotorRun(ARM_MOTOR_PORT,-speed)
    sleep(time)
    bot.encoderMotorRun(ARM_MOTOR_PORT,0)
    
def lower_claw(speed, time):
    bot.encoderMotorRun(ARM_MOTOR_PORT,speed)
    sleep(time)
    bot.encoderMotorRun(ARM_MOTOR_PORT,0)
    
def tighten_claw(speed, time):
    bot.encoderMotorRun(CLAW_MOTOR_PORT,-speed)
    sleep(time)
    bot.encoderMotorRun(CLAW_MOTOR_PORT,0)
    
def loosen_claw(speed, time):
    #print("check")
    bot.encoderMotorRun(CLAW_MOTOR_PORT,speed)
    sleep(time)
    bot.encoderMotorRun(CLAW_MOTOR_PORT,0)

# these are the preset functions to pickup and drop the blocks
# these are dependant on the above claw functions, so do not change those if you want these values to stay relevant.

def pickup_item():
    #print("pickup item")
    lower_claw(50,4)
    tighten_claw(15,3.5)
    raise_claw(50,3.9)
    
def put_down_item():
    #print("put down item")
    lower_claw(50,4)
    loosen_claw(30,2.6)
    raise_claw(50,3.9)
    
def drop_item():
    #print("drop item into bowl")
    lower_claw(50,2)
    loosen_claw(30,2.6)
    raise_claw(50,1.9)
    
    
# may be useful to call after putting a block down
def turn_around():
    print("turn 180 degrees")
    
