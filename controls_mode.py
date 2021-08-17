#! /usr/bin/python3
import motion
import tty, sys, termios

## Note: to exit the program, press 'q'
## Don't do control-c until you press 'q'
## If you just do control-c, then you won't be able to type in the terminal
## and you will have to close the terminal and reopen it in order to type

# controls
forward = "w"
backward = "s"
left = "a"
right = "d"
claw_up = "i"
claw_down = "k"
claw_tight = "j"
claw_loose = "l"

# set up for reading keyboard inputs
filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)

# initialize input variable
input = 0

# main function
while True:
    
    # read inputs from keyboard
    input = sys.stdin.read(1)[0]
    
    # press 'q' to quit
    if input == "q":
        break
    
    # use controls to move in controls mode
    if input == forward:
        motion.move_forward(10,30,4)
    elif input == backward:
        motion.move_backward(10,30,4)
    elif input == left:
        motion.turn_left(1,1)
    elif input == right:
        motion.turn_right(1,1)
    elif input == claw_up:
        motion.raise_claw(30,1.5)
    elif input == claw_down:
        motion.lower_claw(30,1.5)
    elif input == claw_tight:
        motion.tighten_claw(30,1.5)
    elif input == claw_loose:
        motion.loosen_claw(30,1.5)
        

# reset input setting, otherwise won't be able to type in terminal
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)

print("now you can do control-c")
    