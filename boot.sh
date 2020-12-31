#!/bin/bash
# edit /etc/xdg/lxsession/LXDE-pi/autostart
# Or create ~/.config/lxsession/LXDE-pi/ and copy autostart there
# Put in:
#     @lxterminal -e "/home/pi/raspberry-pi-devastator-robot/boot.sh"
/usr/bin/python /home/pi/raspberry-pi-devastator-robot/src/robot.py &
