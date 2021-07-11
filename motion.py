#! /usr/bin/python3
from megapi import *
from time import sleep

bot = MegaPi()
bot.start()

LF_MOTOR_PORT = 1
RR_MOTOR_PORT = 2
ARM_MOTOR_PORT = 3
CLAW_MOTOR_PORT = 4

def move_forward(speed, time):
    print("move forward")
 
def move_backward(speed, time):
    print("move backward")
    
def turn_right(speed, time):
    print("turn right")
    
def turn_left(speed, time):
    print("turn left")
    
def stop():
    print("stop")
    
def backupAndRotate():
    move_backward(1,1)
    turn_right(1,1)
    
def raise_claw(speed, time):
    print("raise claw")
    
def lower_claw(speed, time):
    print("lower claw")
    
def tighten_claw(speed, time):
    print("tighten claw")
    
def loosen_claw(speed, time):
    print("loosen claw")


    
        
    
