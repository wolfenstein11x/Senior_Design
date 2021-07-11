#! /usr/bin/python3
from megapi import *
from time import sleep

bot = MegaPi()
bot.start()

# these numbers will change when we get the new connectors
LF_MOTOR_PORT = 2
RR_MOTOR_PORT = 4
ARM_MOTOR_PORT = 3
CLAW_MOTOR_PORT = 4

def move_forward(left_speed, right_speed, time):
    bot.encoderMotorRun(LF_MOTOR_PORT, -left_speed)
    bot.encoderMotorRun(RR_MOTOR_PORT, right_speed)
    sleep(time)
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)
 
def move_backward(left_speed, right_speed, time):
    bot.encoderMotorRun(LF_MOTOR_PORT, left_speed)
    bot.encoderMotorRun(RR_MOTOR_PORT, -right_speed)
    sleep(time)
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)
    
def turn_right(speed, time):
    print("turn right")
    
def turn_left(speed, time):
    print("turn left")
    
def stop():
    print("stop")
    
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
    bot.encoderMotorRun(CLAW_MOTOR_PORT,speed)
    sleep(time)
    bot.encoderMotorRun(CLAW_MOTOR_PORT,0)

def pickup_item():
    print("pickup item")
    lower_claw(0,0)
    tighten_claw(0,0)
    raise_claw(0,0)
    
    # delay for demonstration purposes only
    #sleep(1)
    
def put_down_item():
    print("put down item")
    lower_claw(0,0)
    loosen_claw(0,0)
    raise_claw(0,0)
    
# may be useful to call after putting a block down
def turn_around():
    print("turn 180 degrees")
    
