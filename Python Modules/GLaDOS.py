import webiopi
import time
from threading import Timer
import sys
sys.path.insert(0, '/home/pi/glados_interface/python')
import rc_switch
import door
import esp
import infrared
import pc_control
import heater
import subprocess 

from datetime import datetime
import json

#Pin Variables#
GPIO = webiopi.GPIO

SERVO_PIN = 27
SERVO_STATUS_PIN = 24
OUTDOOR_PIN = 25
TRANSMITTER_PIN = 1 # GPIO.1 = pin 18
PC_ADDRESS = "192.168.1.20"
ESP8266_ADDRESS = "192.168.1.21"
DOOR_STATUS_PIN = 4
INFRARED_PIN = 23 #just for reference, we set-up the pin while installing lirc (both for transmitter and receiver)
HEATER_SOCKET = 3 



def setup():
		gla = GLaDOS(1)
		sysr = subprocess.Popen("nohup", "sudo python","/home/pi/glados_core/interface/python/system_restart.py") # call subprocess


def destroy():
		gla.terminate()


class GLaDOS():
	def __init__(self,dbug):
		if dbug == 1:
			webiopi.setDebug()

		do = door.Doors(SERVO_PIN,OUTDOOR_PIN,DOOR_STATUS_PIN,SERVO_STATUS_PIN)
		ap = esp.Api(ESP8266_ADDRESS)
		inf = infrared.Infrared(INFRARED_PIN)
		pc = pc_control.Pc(PC_ADDRESS)
		rc1 = rc_switch.Rsiwtch(1,TRANSMITTER_PIN) #1=socketnumber
		rc2 = rc_switch.Rsiwtch(2,TRANSMITTER_PIN)
		he = heater.Heater(HEATER_SOCKET,TRANSMITTER_PIN)



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
	do.up_door()
	if enter == 1: #i am entering the house
		do.inside = True
		do.down_door()
		if pc.status == 0:
			ap.turn_on_pc
		#
		if (datetime.now().time().hour > 6):
			ap.set_status("digital","left_light",enter)
			ap.set_status("digital","right_light",enter)
		ap.set_status(digital,"tv-hifi",enter)
		inf.send(HIFI,"KEY_POWER")
		inf.send(HIFI,"KEY_COMPUTER")
	
	else: #enter = 0 <=> I am exiting the house
		do.inside = False 
		#
		ap.set_status("digital","left_light",enter)
		ap.set_status("digital","right_light",enter)
		ap.set_status(digital,"tv-hifi",enter)
		#
		Timer(10,do.alert)

@macro
def gday():
	if pc.status == 0:
		ap.turn_on_pc
	ap.set_status("digital","left_light",1)
	ap.set_status("digital","right_light",1)
	ap.set_status(digital,"tv-hifi",1)
	inf.send(HIFI,"KEY_POWER")
	inf.send(HIFI,"KEY_COMPUTER")
	Timer(5,pc.log_in)
	Timer(10,pc.music,["morning","chill"])
@macro
def gnight():
	ap.set_status("digital","left_light",0)
	ap.set_status("digital","right_light",0)
	ap.set_status(digital,"tv-hifi",0)

@macro
def heater(mode,time):
	if mode == 1:
		he.turn_on(time) #time in seconds
	elif mode == 0:
		he.turn_off()


@macro
def lights(number,function): #function = 1 or 0, on/off
	if number == 1:
		rc1.send(function)
	elif number == 2:
		rc2.send(function)
	elif number == 3:
		ap.set_status("digital","left_light",function)
	elif number == 4:
		ap.set_status("digital","right_light",function)

def status():
	a = ap.get_status("digital","left_light")
	b = ap.get_status("digital","right_light")
	el.time = he.elapsed_time()
	
	return json.dumps([rc1.status,rc2.status,a,b,do.inside,he.heater_status,el.time])

@macro 
def desktop_pc(function):
	if function == 0: 
		pc.turn_off()
	if function == 1:
		ap.turn_on_pc

	if function == "status":
		status = pc.status()
		return  json.dumps ([status])


