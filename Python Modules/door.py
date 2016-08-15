import webiopi
from threading import Timer
import pygame

GPIO = webiopi.GPIO

class Doors():
	def __init__(self,servo_pin,outdoor_pin,door_status_pin,servo_power): #we want the servo to be powered-off when it's in standby so as not to jiggle. We control thr power line with a mosfet or optocoupler.
		self.servo = servo_pin
		self.outdoor= outdoor_pin
		self.d_status = door_status_pin
		self.servo_power = servo_power
		self.inside = 1 #whether I am in or out
	 
	def up_door(self,function):
		GPIO.digitalWrite(self.servo_power, GPIO.HIGH)
		
		if function == "open":
			for angle in range(-90,90):
				webiopi.debug(-angle)
				GPIO.pwmWriteAngle(self.servo,-angle)
			self.update_status(0) #initialize self.counter ,pass it as an argument
		elif function == "close":
			for angle in range(-90,90):
				GPIO.pwmWriteAngle(self.servo,angle)
	    
		GPIO.digitalWrite(self.servo_power, GPIO.LOW)
	
	def down_door(self,function): #function variable tells whether we want to open or close the door when we call the down_door
		if function == "open":
			GPIO.digitalWrite(self.outdoor, GPIO.HIGH)
			Timer(3,self.down_door,["close"])
		elif function == "close":
			GPIO.digitalWrite(self.outdoor, GPIO.LOW)

	def check_status(self): #for up.door which uses the servo
		if (GPIO.digitalRead(d_status) == GPIO.LOW):
			return "open"
		elif (GPIO.digitalRead(d_status) == GPIO.HIGH):
			return "close"
	
	def update_status(self,counter): # I want self.counter to persist each time I call the function, I need to detect an close/open/close sequence.
		if (self.check_status() == "close"):
			if(counter == 0):
				counter +=1

			elif(self.counter == 2):
				self.up_door("close")
				return None

			Timer(1,self.update_status(counter))
		
		elif (self.check_status() == "open"):
			if(self.counter == 1):
				counter +=1
			Timer(1,self.update_status(counter))
	
	def alert(self): #checks whethere status_open = true and plays the alert sound, it calls it self each time
		if not self.inside:
			if self.check_status()== "open":
				pygame.mixer.init()
				pygame.mixer.music.load("path/to/alert.mp3")
				pygame.mixer.music.play()
				while pygame.mixer.music.get_busy() == True:
					continue
				self.alert()
			else:
				Timer(1,self.alert)
		else:
			return None


