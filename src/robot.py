# import curses and GPIO
import curses
import os # Added so we can shut down OK
import time # Import time module
import threading # If we want things to happen after a button press, and carry on listening, we need threads.
import RPi.GPIO as GPIO

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
GPIO.setup(7,GPIO.OUT)
GPIO.output(7,True)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)

# We have a thread which we nullify to stop blinking
blink_thread = None

def toggle_function(sleep_time, pins, op):
    '''
    This function simply toggles between off and on all the
    pins in the pin list and sleeps for sleep time between.
    '''
    while blink_thread:
        for pin in pins:
            GPIO.output(pin, False)
        if op:
            for pin in op:
                GPIO.output(pin, True)

        time.sleep(sleep_time)

        for pin in pins:
            GPIO.output(pin, True)
        if op:
            for pin in op:
                GPIO.output(pin, False)

        time.sleep(sleep_time)

    # Finally leave them on
    for pin in pins:
        GPIO.output(pin, True)
    if op:
        for pin in op:
            GPIO.output(pin, True)

def process_movement(character):
    if character == curses.KEY_UP:
        GPIO.output(16, False)
        GPIO.output(18, True)
        GPIO.output(13, False)
        GPIO.output(15, True)

    elif character == curses.KEY_DOWN:
        GPIO.output(16, True)
        GPIO.output(18, False)
        GPIO.output(13, True)
        GPIO.output(15, False)
    elif character == curses.KEY_RIGHT:
        GPIO.output(16, False)
        GPIO.output(18, True)
        GPIO.output(13, True)
        GPIO.output(15, False)
    elif character == curses.KEY_LEFT:
        GPIO.output(16, True)
        GPIO.output(18, False)
        GPIO.output(13, False)
        GPIO.output(15, True)
    elif character == 10: # Okay = stop!
        GPIO.output(16, False)
        GPIO.output(18, False)
        GPIO.output(13, False)
        GPIO.output(15, False)

# Main function which processes key presses.
try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == ord('S'): # Added for shutdown on capital S
            os.system ('sudo shutdown now') # shutdown right now!
        elif char == ord('b'):  # Start/stop lights blinking
            if blink_thread:
                blink_thread = None
            else:
                blink_thread = threading.Thread(name="Blinker", target=toggle_function, args=(0.5, [7,11], None, ))
                blink_thread.start()

        elif char == ord('a'):  # Start/stop lights blinking, alternate
            if blink_thread:
                blink_thread = None
            else:
                blink_thread = threading.Thread(target=toggle_function, args=(0.5, [7], [11], ))
                blink_thread.start()
        else:
            process_movement(char)

finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    

