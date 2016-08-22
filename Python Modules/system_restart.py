import httplib
import os
from threading import Timer
import Selenium

class SystemRestart():

	def __init__(self,interval):

		Timer(interval*60,self.system_check).start()
		self.system_check()

	def have_internet(self):
	    conn = httplib.HTTPConnection("www.google.com")
	    try:
	        conn.request("HEAD", "/")
	        return True
	    except:
	        return False


	def site_online(self):
		conn = httplib.HTTPConnection("192.168.1.19:8000")
	    try:
	        conn.request("HEAD", "/")
	        return True
	    except:
	        return False


	def system_check(self):
		if self.have_internet() == False:
			self.router_reboot() #Record it using selinium-->export to rpi + modifications as in 
								 #https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=129320 Selinium in headless rpi
		elif self.site_online() == False:
			os.system("sudo reboot")
		else:
			return True
	def router_reboot(self):
		pass


if __name__ == '__main__':
	sr = SystemRestart(10)