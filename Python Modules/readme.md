
##Python Modules 

The python modules consist of the server-site side of the project. Along with the HTML server, webiopi runs GLaDOS.py as the main script that coordinates all actions(e.g macro's)

####GLaDOS has many features,each consisting of a module in different script files. 

##Door.py: 
It's the script that controls the building's door(down_door) and appartment's door(up_door).

##esp.py : 
It communicates with various esp8266 via REST calls, esp8266 is a IoT SOC that can be programmed through the Arduino environment.

##heater.py: 
Module that controls the boiler and it's timer. The boiler is controled via a RF switch.

##infrared.py : 
A simple shell command caller to use lirc through python

##pc_control.py: 
This script will call python2 scripts that use vncdotool to control remotely my desktop. vncdotool apparently works only with python2.

##rc_send.py: 
python2 scripts that used pi_switch library to send rf signals, it's called via shell commands from other scripts.

##system_restart: 
Thanks to selenium and httplib it will check whether rpi2 has internet or the server is online and will either reboot the router or reboot the rpi.
