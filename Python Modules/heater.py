import sys
import webiopi
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
		self.heater_start = time.time()
		webiopi.debug("heater will turn of in %d seconds" %runtime)
		self.heat_timer = Timer(self.runtime, self.turn_off)
		self.heat_timer.start()
		ret=call(["sudo python /home/pi/glados_interface/python/rc_send.py %s %s %s" % (str(self.tran_pin),"1",str(self.socket_number))],shell=True)
		if ret !=0:
			webiopi.debug("can't call rc_send")
		self.heater_status = 1
	
	def turn_off(self):
		webiopi.debug("turning off heater....")
		ret=call(["sudo python /home/pi/glados_interface/python/rc_send.py %s %s %s" % (str(self.tran_pin),"0",str(self.socket_number))],shell=True)
		if ret !=0:
			webiopi.debug("can't call rc_send")
		if self.heater_status == 1:
			if self.heat_timer.is_alive():
				webiopi.debug("Canceling Timer")
				self.heat_timer.cancel()
				webiopi.debug("TIMER IS NOW:")
		self.heater_status = 0
	def elapsed_time(self):
		if self.heater_status == 0:
			return 0
		else:
			elapsed = time.time() - self.heater_start #elapsed =16 sec
			sec_end = int(self.runtime - elapsed) #till end is runtime(e.g 9000sec) - elapsed(e.16sec)
			return sec_end




