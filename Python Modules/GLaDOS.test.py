import webiopi
import time
from threading import Timer
import sys
sys.path.insert(0, '/home/pi/glados_interface/python')
import subprocess 

from datetime import datetime
import json

#Pin Variables#
GPIO = webiopi.GPIO

#CONSTANTS

PC_ADDRESS = "192.168.1.20"
ESP8266_ADDRESS = "192.168.1.21"
HEATER_SOCKET = 3 

#PINS

SERVO_PIN = 27
SERVO_STATUS_PIN = 24
OUTDOOR_PIN = 25
TRANSMITTER_PIN = 1 # GPIO.1 = pin 18
DOOR_STATUS_PIN = 4
INFRARED_PIN = 23 #just for reference, we set-up the pin while installing lirc (both for transmitter and receiver)





def setup():
		print("Setup")
		gla = GLaDOS(1)
		print("started Glados")
		 # call subprocess


def destroy():
		gla.terminate()


class GLaDOS():
	def __init__(self,dbug):
		if dbug == 1:
			webiopi.setDebug()

		



		GPIO.setFunction(SERVO_STATUS_PIN, GPIO.IN)
		GPIO.setFunction(OUTDOOR_PIN, GPIO.OUT)
		GPIO.setFunction(SERVO_PIN, GPIO.PWM)
		GPIO.setFunction(DOOR_STATUS_PIN, GPIO.IN)	
		GPIO.digitalWrite(OUTDOOR_PIN, GPIO.LOW)
		do.up_door("close")
	
	def terminate(self):
		do.up_door()
		he.turn_off()


 #~~~~~~~~~~~~~~~~MACROS MACROS MACROS MACROS MACROS MACROS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

@macro
def house(enter):
	webiopi.debug("house")

@macro
def gday():
	webiopi.debug("gday")
@macro
def gnight():
	webiopi.debug("gnight")

@macro
def heater(mode,time):
	webiopi.debug("heater")


@macro
def lights(number,function): #function = 1 or 0, on/off
	print("lights "+ number " " + function)

def status():
	return json.dumps([1,1,1,0,1,1,1])

@macro 
def desktop_pc(function):
	print("pc "+ function )


