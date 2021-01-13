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
global blink_thread
blink_thread = None
global blink_time
blink_time = 0.5

def toggle_function(sleep_time, pins, op, leave_on):
    '''
    This function simply toggles between off and on all the
    pins in the pin list and sleeps for sleep time between.

    It can be used for instance to blink lights or make the motors
    enter a jerky mode.
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

    # Finally leave them at leave_on
    for pin in pins:
        GPIO.output(pin, leave_on)
    if op:
        for pin in op:
            GPIO.output(pin, leave_on)

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

def stop():
    GPIO.output(16, False)
    GPIO.output(18, False)
    GPIO.output(13, False)
    GPIO.output(15, False)

def process_code(code, pins):

    code_applied = False

    # If there is no code, we are done
    if not code:
        return

    # "-t0.5[ENTER]" to change the blink time or jerk time
    if code.startswith("-t"):
        global blink_time
        blink_time = float(code[2:10])
        code_applied = True

    if code_applied: # Tell user we updated the code
        for pin in pins:
            GPIO.output(pin, False)
        time.sleep(0.5)
        for pin in pins:
            GPIO.output(pin, True)



# Main function which processes key presses.
def main():
    try:

        code = ""
        '''
        They can type whole codes or cursor commands. For example
        ENTER or ok stops the robot but if they have previously typed
        t0.5 then the blink time will be changed to 0.5 as well. Each 
        time a char command is accepted, the 
        '''

        commands = ['q', 'S', 'b', 'a', 'j', curses.KEY_ENTER, 10, 13,
                    curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]
        ''' 
        All the possible direct commands. Everything else is a code.
        '''

        global blink_thread, blink_time
        '''
        State is held in globals. This is a small script.
        '''

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
                    blink_thread = threading.Thread(name="Blinker", target=toggle_function, args=(blink_time, [7,11], None, True, ))
                    blink_thread.start()

            elif char == ord('a'):  # Start/stop lights blinking, alternate
                if blink_thread:
                    blink_thread = None
                else:
                    blink_thread = threading.Thread(target=toggle_function, args=(blink_time, [7], [11], True, ))
                    blink_thread.start()

            elif char == ord('j'):  # Start/stop motors jerking. You might want to do '-t5[ENTER]' to change the time.
                if blink_thread:
                    blink_thread = None
                else:
                    blink_thread = threading.Thread(target=toggle_function, args=(blink_time, [13,16], [18,15], False, ))
                    blink_thread.start()

            elif char == curses.KEY_ENTER or char == 10 or char == 13:
                stop()
                process_code(code, [7,11])

            else:
                process_movement(char)

            if char in commands:
                code = ''
                continue

            # They might be building a command like "-t0.5(ENTER)" to change the blink time.
            code = code+str(char)


    finally:
        #Close down curses properly, inc turn echo back on!
        curses.nocbreak(); screen.keypad(0); curses.echo()
        curses.endwin()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
    

