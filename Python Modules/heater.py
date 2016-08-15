import sys
import webiopi
sys.path.insert(0, '/home/pi/glados_interface/python')
import json
import time
from subprocess import call
from threading import Timer

class Heater():
	def __init__(self,socket_number,tran_pin):
		self.heater_status = 0
		self.socket_number = socket_number
		self.tran_pin = tran_pin
		#self.rc = rc_switch.Rcswitch(socket_number,tran_pin)


	def turn_on(self,runtime): #time in seconds
		runtime = float(runtime)
		self.runtime = runtime
		runtime = runtime * 60
		self.heater_start = time.time()
		Timer(runtime, self.turn_off).start()
		ret=call(["sudo python /home/pi/glados_interface/python/rc_send.py %s %s %s" % (str(self.tran_pin),"0",str(self.socket_number))],shell=True)
		if ret !=0:
			webiopi.debug("can't call rc_send")
		#self.rc.send(self.socket_number,"on")
		self.heater_status = 1
	def turn_off(self):
		ret=call(["sudo python /home/pi/glados_interface/python/rc_send.py %s %s %s" % (str(self.tran_pin),"0",str(self.socket_number))],shell=True)
		if ret !=0:
			webiopi.debug("can't call rc_send")
		self.heater_status = 0

	def elapsed_time(self):
		if self.heater_status == 0:
			return 0
		else:
			elapsed = time.time() - self.heater_start #elapsed =16 sec
			sec_end = int(self.runtime -elapsed) #till end is runtime(e.g 9000sec) - elapsed(e.16sec)

			return sec_end




