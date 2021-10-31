from megapi import *
from time import sleep
# import ball_following_function as ball
    

bot = MegaPi()
bot.start()
#bot.start('/dev/ttyUSB0')

# left front wheel motor is connected to port 1
# right rear wheel motor is connected to port 2
# arm motor is connected to port 3
# claw motor is connected to port 4
LF_MOTOR_PORT = 1
RR_MOTOR_PORT = 2
ARM_MOTOR_PORT = 3
CLAW_MOTOR_PORT = 4

def move_forward():
    bot.encoderMotorRun(RR_MOTOR_PORT,40)
    bot.encoderMotorRun(LF_MOTOR_PORT,-40)

def reverse():
    bot.encoderMotorRun(RR_MOTOR_PORT, -40)
    bot.encoderMotorRun(LF_MOTOR_PORT, 40)

def turn_right():
    bot.encoderMotorRun(RR_MOTOR_PORT, -15)    #-16
    bot.encoderMotorRun(LF_MOTOR_PORT, 0)     #-8
    
def turn_left():
    bot.encoderMotorRun(RR_MOTOR_PORT, 0)     #8
    bot.encoderMotorRun(LF_MOTOR_PORT, 15)    #16

def turn_right_fast():
    bot.encoderMotorRun(RR_MOTOR_PORT, -40)    #-16
    bot.encoderMotorRun(LF_MOTOR_PORT, -30)     #-8
    
def turn_left_fast():
    bot.encoderMotorRun(RR_MOTOR_PORT, 30)     #8
    bot.encoderMotorRun(LF_MOTOR_PORT, 40)    #16

def lower_arm():
    bot.encoderMotorRun(ARM_MOTOR_PORT, 60)
    sleep(3)
    bot.encoderMotorRun(ARM_MOTOR_PORT, 20)
    sleep(0.4)
    bot.encoderMotorRun(ARM_MOTOR_PORT,00)

def raise_arm():
    bot.encoderMotorRun(ARM_MOTOR_PORT, -70)
    sleep(3.2)
    bot.encoderMotorRun(ARM_MOTOR_PORT, -20)
    sleep(0.3)
    bot.encoderMotorRun(ARM_MOTOR_PORT,00)
    
def close_gripper():
    bot.encoderMotorRun(CLAW_MOTOR_PORT, -20)
    sleep(2)
    bot.encoderMotorRun(CLAW_MOTOR_PORT, 0)
    
def open_gripper():
    bot.encoderMotorRun(CLAW_MOTOR_PORT, 20)
    sleep(2.8)
    bot.encoderMotorRun(CLAW_MOTOR_PORT, 0)

def stop_cmd():
    bot.encoderMotorRun(1, 0)
    bot.encoderMotorRun(2, 0)
    bot.encoderMotorRun(3, 0)
    bot.encoderMotorRun(4, 0)

def search():
    turn_left()
    sleep(3)
#    turn_right()
#    sleep(2)
    stop_cmd()

def quit_now():
    exit()
    
def err():
    print('Command not recognized!')


# commmand dictionary
cmd_dict = {
            'search'  : search,
            'right'   : turn_right,
            'left'    : turn_left,
            'right_fast': turn_right_fast,
            'left_fast' : turn_left_fast,
            'forward' : move_forward,
            'back'    : reverse,
            'lower'   : lower_arm,
            'raise'   : raise_arm,
            'close'   : close_gripper,
            'open'    : open_gripper,
            'stop'    : stop_cmd,
            'quit'    : exit
            }

