import sys
sys.path.insert(0, '/home/pi/glados_interface/python')
import json
import rc_switch
import time

class Heater():
	def __init__(self,socket_number,tran_pin):
		self.heater_status = 0
		
		self.rc = rc_switch.Rcswitch(socket_number,tran_pin)


	def turn_on(runtime): #time in seconds
		runtime = float(runtime)
		runtime = runtime * 60
		self.heater_start = time.time()
		Timer(time, self.heateroff).start()
		self.rc.send(self.socket_number,"on")
		self.heater_status = 1

 	def turn_off(self):
 		self.rc.send(self.socket_number,"off")
 		self.heater_status = 0

 	def elapsed_time(self):
 		if self.heater_status == 0:
 			return 0
 		else:
 			elapsed = time.time() - self.heater_start
 			return int(elapsed)




