# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import os #added so we can shut down OK
import time #import time module

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)

# 16 and 18 are not on by defaut.
GPIO.setup(16,GPIO.OUT) # 7 in his
GPIO.setup(18,GPIO.OUT) # 11 in his

# Keep 13 and 15 the same
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

# LED
GPIO.setup(11,GPIO.OUT)
GPIO.output(11,True)


# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        if char == ord('S'): # Added for shutdown on capital S
            os.system ('sudo shutdown now') # shutdown right now!
        elif char == curses.KEY_UP:
            GPIO.output(16,False)
            GPIO.output(18,True)
            GPIO.output(13,False)
            GPIO.output(15,True)
        elif char == curses.KEY_DOWN:
            GPIO.output(16,True)
            GPIO.output(18,False)
            GPIO.output(13,True)
            GPIO.output(15,False)
        elif char == curses.KEY_RIGHT:
            GPIO.output(16,False)
            GPIO.output(18,True)
            GPIO.output(13,True)
            GPIO.output(15,False)
        elif char == curses.KEY_LEFT:
            GPIO.output(16,True)
            GPIO.output(18,False)
            GPIO.output(13,False)
            GPIO.output(15,True)
        elif char == 10:
            GPIO.output(16,False)
            GPIO.output(18,False)
            GPIO.output(13,False)
            GPIO.output(15,False)
             
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    

