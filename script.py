# Imports
import webiopi
import time
from threading import Timer
from wakeonlan import wol 
import pi_switch
import json
import os
from vncdotool import api
from subprocess import call



#Codes for sockets:
#socket_1: ON:000000010100010001010101 ||OFF:000000010100010001010100 
#socket_2: ON:000000010101000001010101 ||OFF:000000010101000001010100
#socket_3: ON:000000010001010001010101 ||OFF:000000010001010001010100
#socket_4: ON:000000000101010001010101 ||OFF:000000000101010001010100





# Enable debug output
webiopi.setDebug()

# Retrieve GPIO lib
GPIO = webiopi.GPIO
SERVO  = 18
OutDoor = 25

# Called by WebIOPi at script loading
def setup():
    webiopi.debug("Script with macros - Setup")
    global Servo
    Servo = 1
    GPIO.setFunction(OutDoor, GPIO.OUT)
    GPIO.setFunction(SERVO, GPIO.PWM)
    CloseUDoor()   # set to 0 (neutral)
    GPIO.digitalWrite(OutDoor, GPIO.LOW)
    global Heater
    global hostname
    global sender
    Heater = 0
    hostname = "192.168.1.20" #example
    sender = pi_switch.RCSwitchSender()
    sender.enableTransmit(0) 

# Called by WebIOPi at server shutdown
def destroy():
    webiopi.debug("Script with macros - Destroy")
    GPIO.setFunction(SERVO, GPIO.PWM)
    CloseUDoor()
    OffHeater()

    # Reset GPIO functions


@webiopi.macro
def PCON(enter):
    webiopi.debug("PCON")
    wol.send_magic_packet('1c:6f:65:c5:c3:68')
    webiopi.debug(enter)
    if enter == 1:
        webiopi.debug("timer")
        Timer(5*60, intro(1)).start()

def intro(on):
    if on == 1:
        client = api.connect('192.168.1.20')
        client.keyPress('enter')
        client.keyPress('enter')
        client.pause(1.5)
        for k in '1556':
            client.keyPress(k)
        Timer(1*60, intro2).start()
    else:
        intro2()
def intro2():
    client = api.connect('192.168.1.20')
    client.mouseMove(80,1050)
    client.mousePress(1)
    for i in "run":
       client.keyPress(i)
    client.pause(0.5)
    client.keyPress("enter")
    client.pause(0.6)
    for i in "F:\Odys\Music\Intro.xspf":
        client.keyPress(i)
    client.keyPress("enter")


@webiopi.macro
def OpenDoors(argument):
    webiopi.debug("mpika doors geniko")
    DownDoor()
    UpDoor(argument)

def DownDoor():
    webiopi.debug("OpenDdoor")
    GPIO.digitalWrite(OutDoor, GPIO.HIGH)
    Timer(3, CloseDDoor).start()


def UpDoor(status):
    GPIO.setFunction(SERVO, GPIO.PWM)
    webiopi.debug("OpenUdoor=")
    global Servo
    webiopi.debug(Servo)
    if Servo == 0:
        notify_status = "Door Unlocked"
        alert(notify_status)
        for angle in range(-90,90):
            webiopi.debug(-angle)
            #webiopi.sleep(0.01)
            GPIO.pwmWriteAngle(SERVO,-angle)
        Servo = 1
        if status == "enter":
            Timer(30,CloseUDoor).start()
        elif status == "leave":
            Timer(10,CloseUDoor).start()
        elif status == "knock":
            Timer(60,CloseUDoor).start()

def CloseDDoor():
    webiopi.debug("closeDdoor")
    GPIO.digitalWrite(OutDoor, GPIO.LOW)

def CloseUDoor():
    webiopi.debug("closeUdoor")
    global Servo
    if Servo ==1:
        status = "Door Locked"
        alert(status)
        for angle in range(-90,90):
            webiopi.debug(angle)
            GPIO.pwmWriteAngle(SERVO,angle)
        Servo = 0
        GPIO.setFunction(SERVO, GPIO.IN)


@webiopi.macro
def HouseEnter():
    LightGroup1(1)
    LightGroup2(1)
    OpenDoors("enter")
    webiopi.debug("Pc-on-lights on")
    response = os.system("ping -c 1 " + hostname)
    if response != 0:
        PCON(1)
    else:
        intro(1)

@webiopi.macro
def LeavEHouse():
    webiopi.debug("lightsoff");
    LightGroup1(0)
    LightGroup2(0)
    UpDoor("leave")
    #Turn off pc, lights


@webiopi.macro
def OnHeater(time): # Turn on Heater and call Timer function which will turn off the Heater
    global Heater 
    Heater = 1
    LightGroup3(1)
    time = float(time)
    time = time * 60
    webiopi.debug("heater OK, time")
    webiopi.debug(time)
    Timer(time, OffHeater).start()
    status = "Boiler is on %"
    alert("Boiler is on for %f minutes" %(time/60.0))

@webiopi.macro
def OffHeater():
    global Heater
    LightGroup3(0)
    Heater = 0
    alert("Boiler is Off")


@webiopi.macro
def HeaterStatus():
    webiopi.debug("heater =")
    webiopi.debug(Heater)
    return json.dumps ([Heater])


def alert(status):
   call(["/usr/bin/notify_Weavedwebiopi8000.sh", "0",status, "Update"])# pathainei egefaliko mpainei se loupa, perito edo,xrisimo genika na to koitakso

def LightGroup1(on):
    if on:
        sender.send("000000010100010001010101")
    else:
        sender.send("000000010100010001010100")
def LightGroup2(on):
    if on:
        sender.send("000000010101000001010101")
    else:
        sender.send("000000010101000001010100")
def LightGroup3(on):
    if on:
        sender.send("000000010001010001010101")
    else:
        sender.send("000000010001010001010100")
