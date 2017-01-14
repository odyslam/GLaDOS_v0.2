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
		webiopi.debug("mpika up_door")
		webiopi.debug(self.servo_power)
		Timer(2,GPIO.digitalWrite,[self.servo_power, GPIO.LOW]).start()
		
		if function == 1:
			webiopi.debug("mpika sto open")

			for angle in range(-90,90):

				webiopi.debug(-angle)
				GPIO.pwmWriteAngle(self.servo,-angle)
			self.update_status(0) #initialize self.counter ,pass it as an argument
		elif function == 0:
			for angle in range(-90,90):
				webiopi.debug(angle)
				GPIO.pwmWriteAngle(self.servo,angle)
	    
	
	def down_door(self,function): #function variable tells whether we want to open or close the door when we call the down_door
		if function == 1:
			GPIO.digitalWrite(self.outdoor, GPIO.HIGH)
			Timer(3,self.down_door,[0]).start()
		elif function == 0:
			GPIO.digitalWrite(self.outdoor, GPIO.LOW)

	def check_status(self): #for up.door which uses the servo
		if (GPIO.digitalRead(self.d_status) == GPIO.LOW):
			return 1 #open
		elif (GPIO.digitalRead(self.d_status) == GPIO.HIGH):
			return 0 #close
	
	def update_status(self,counter):
		webiopi.debug("counter:%d" %counter) # I want self.counter to persist each time I call the function, I need to detect an close/open/close sequence.
		if (self.check_status() == 0): #update_status polls the door_status pin to detect an "close-open-close" sequence of the door.
			if(counter == 0): 		   #The door starts closed but unlocked(counter=0), I open it and enter the house(counter=1), then i close the door(counter=2) and the mechanism locks.
				counter +=1

			elif(counter == 2):
				counter +=1

			elif(counter == 3):
				self.up_door(0)
				return 
				#Timer(1,self.up_door,[0]).start()

			Timer(0.5,self.update_status,[counter]).start()
		
		elif (self.check_status() == 1):
			if(counter == 1):
				counter +=1
			Timer(0.5,self.update_status,[counter]).start()
	
	def alert(self): #checks whethere status_open = true and plays the alert sound, it calls it self each time
		if not self.inside:
			if self.check_status()== 1:
				pygame.mixer.init()
				pygame.mixer.music.load("/home/pi/glados_interface/resources/alert1.mp3")
				pygame.mixer.music.play()
				while pygame.mixer.music.get_busy() == True:
					continue
				self.alert()
			else:
				Timer(1,self.alert).start()
		else:
			return None


