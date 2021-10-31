#! /usr/bin/python3

import robot_move_definitions as rd
import time
from megapi import *


bot = MegaPi()
bot.start()


bot.encoderMotorRun(4, 10)
bot.encoderMotorRun(2, -10)
time.sleep(2)
bot.encoderMotorRun(4, 0)
bot.encoderMotorRun(2, 0)

print("done")



