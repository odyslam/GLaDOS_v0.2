### Last edit 12/3
import webiopi
import time
from threading import Timer
import sys
import subprocess 
import os
import signal
from datetime import datetime
import json

#import glados modules
sys.path.insert(0, '/home/pi/glados_interface/python')
import door
import esp
import infrared
import pc_control
import heater

#Pin Variables#
GPIO = webiopi.GPIO

#CONSTANTS

PC_ADDRESS = "192.168.1.20"
ESP8266_ADDRESS = "http://192.168.1.30"
HEATER_SOCKET = 3 

#PINS

SERVO_PIN = 6
SERVO_STATUS_PIN = 5
OUTDOOR_PIN = 23
TRANSMITTER_PIN = 1 # GPIO.1 = pin 18
DOOR_STATUS_PIN = 22
INFRARED_PIN = 25 
#just for reference, we set-up the pin while installing lirc (both for transmitter and receiver)

# GLobal Instances

do = door.Doors(SERVO_PIN, OUTDOOR_PIN, DOOR_STATUS_PIN, SERVO_STATUS_PIN)
ap = esp.Api(ESP8266_ADDRESS)
inf = infrared.Infrared(INFRARED_PIN)
pc = pc_control.Pc(PC_ADDRESS)
he = heater.Heater(HEATER_SOCKET, TRANSMITTER_PIN)
fb_bot = subprocess.Popen("python /home/pi/glados_interface/bot/fb_bot.py", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) # start bot
# system_monitor.py is run by crontab every X min, now X = 5. 
# Resets log_file every day @12pm

#global variables for sockets and if someone is inside

socket1_status = 0
socket2_status = 0
glo_inside = 0

# setup my GPIOs and their usage
# setup is invoked @start of webiopi servce
def setup():
    webiopi.debug("Setup")
    GPIO.setFunction(SERVO_STATUS_PIN, GPIO.IN)
    GPIO.setFunction(OUTDOOR_PIN, GPIO.OUT)
    GPIO.setFunction(SERVO_STATUS_PIN, GPIO.OUT)
    GPIO.setFunction(SERVO_PIN, GPIO.PWM)
    GPIO.setFunction(DOOR_STATUS_PIN, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.digitalWrite(OUTDOOR_PIN, GPIO.LOW)
    GPIO.digitalWrite(SERVO_STATUS_PIN, GPIO.LOW)
    do.up_door(0) #lock up_door

#destroy is invoked @exit of webiopi service
def destroy(): 
    GPIO.digitalWrite(OUTDOOR_PIN, GPIO.LOW)
    GPIO.digitalWrite(SERVO_STATUS_PIN, GPIO.LOW)
    do.up_door(0) #lock up_door
    he.turn_off() #turn_off boiler
    fb_bot.kill() #kill fb_bot, doesn't work atm
 #~~~~~~~~~~~~~~~~MACROS MACROS MACROS MACROS MACROS MACROS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
@webiopi.macro
def house(enter):
    global glo_inside
    enter = int(enter)
    do.up_door(1)
    lights(1, enter) #office_lights
    ap.set_status("digital", "tv-hifi", enter) 
    if enter == 1:
        glo_inside = 1
        mood = "chill"
        time = 0 
        do.down_door(1)
        if pc.status() == 0:
            ap.turn_on_pc()
        Timer(45, pc.vnc_control, ["log_in", 0, 0]).start()
        inf.send("ADVANCE_ACOUSTIC", "power", 1)
        #next command after power doesn't work,reason uknown
        inf.send("ADVANCE_ACOUSTIC", "input_computer", 1)
        Timer(15, inf.send, ["ADVANCE_ACOUSTIC", "input_computer", 1]).start()
        Timer(25, inf.send, ["ADVANCE_ACOUSTIC", "volume_up", 10]).start()
        hour = int(datetime.now().time().hour)
        if hour >= 22 or hour <= 7:
            webiopi.debug("mpika romance enter")
            mood = "romance"
            lights(3, enter) #left_light
            lights(4, enter) #righ_light
        elif hour >= 16: #I enter home propably exhuasted from class/workout
            lights(3, enter) #left_light
            lights(4, enter) #righ_light
            if hour >= 18:
                time = "night"
        Timer(90, pc.vnc_control, ["music", time, mood]).start()
    else: #enter = 0 <=> I am exiting the house
        glo_inside = 0
        webiopi.debug("leaving house")
        lights(3, enter) #left_light
        lights(4, enter) #righ_light
        
@webiopi.macro
def open_door(door_number): #control appertment's/building's door
    door_number = int(door_number)
    if door_number == 1:
        do.up_door(1)
    elif door_number == 2:
        do.down_door(1)
        do.up_door(1)
@webiopi.macro
def gday(): #Morning Routine
    ap.set_status("digital", "tv-hifi", 1)
    if pc.status() == 0:
        ap.turn_on_pc()
    lights(1, 1) #turn_on office lights
    inf.send("ADVANCE_ACOUSTIC", "power", 1)
    #next command after power doesn't work,reason uknown
    inf.send("ADVANCE_ACOUSTIC", "input_computer", 1)
    Timer(15, inf.send, ["ADVANCE_ACOUSTIC", "input_computer", 2]).start()
    Timer(25, inf.send, ["ADVANCE_ACOUSTIC", "volume_up", 8]).start()
    Timer(40, pc.vnc_control, ["log_in", 0, 0]).start()
    Timer(90, pc.vnc_control, ["music", "morning", "chill"]).start()
@webiopi.macro
def gnight(): #Night-Routine
    lights(1, 0) #office_light
    lights(3, 0) #left_light
    lights(4, 0) #righ_light
    ap.set_status("digital", "tv-hifi", 0)
@webiopi.macro
def heater(mode, time): #control boiler
    mode = int(mode)
    time = int(time)
    if mode == 1:
        webiopi.debug("heater started for : ")
        webiopi.debug(time)
        he.turn_on(time) #time in seconds
    elif mode == 0:
        webiopi.debug("heater stop")
        he.turn_off()
@webiopi.macro
def lights(number, function): #function = 1/0 ==> on/off
    global socket1_status,socket2_status
    sockets = [socket1_status,socket2_status]
    number = int(number)
    function = int(function)
    if number in [1,2]:
        rc_string = "sudo python /home/pi/glados_interface/python/rc_send.py " + str(TRANSMITTER_PIN) + " " + str(function) + " " +  str(number)
        answer = subprocess.Popen(rc_string,shell = True)
        if number == 1:
            socket1_status = function
        elif number == 2:
            socket2_status = function
    elif number == 3:
        ret=ap.set_status("digital","left_light",function)
        webiopi.debug("return value of function:%d is %s" %(function,str(ret)))
    elif number == 4:
        ret=ap.set_status("digital","right_light",function)
        webiopi.debug("return value of function:%d is %s" %(function,str(ret)))
@webiopi.macro
def status():  #Gets the status of all appliances and returns it via REST in json form.
    global glo_inside
    do.inside = glo_inside
    status_dict = {}
    status_dict['l_light'] = ap.get_status("digital", "left_light")
    status_dict['r_light'] = ap.get_status("digital", "right_light")
    status_dict['el_time'] = he.elapsed_time()
    status_dict['o_light'] = socket1_status
    status_dict['he_status'] = he.heater_status
    status_dict['pc_status'] = pc.status()
    status_dict['inside'] = do.inside
    return json.dumps(status_dict,separators=(',', ':'))
@webiopi.macro
def desktop_pc(function):
    function = int(function)
    if function == 0:
        pc.vnc_control("turn_off", 0, 0)
    if function == 1:
        ap.turn_on_pc()
@webiopi.macro
def hifi(function, args=None): #control the hifi system via inf/red led, LIRC library
    args = int(args)
    if function == "power":
        inf.send("ADVANCE_ACOUSTIC", "power", 1)
    elif function == "volume_up":
        inf.send("ADVANCE_ACOUSTIC", "volume_up", args)
    elif function == "volume_down":
        inf.send("ADVANCE_ACOUSTIC", "volume_down", args)
    elif function == "computer":
        inf.send("ADVANCE_ACOUSTIC", "input_computer", 1)
