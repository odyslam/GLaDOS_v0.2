from subprocess import call

class Infrared():
	def __init__(self,led_pin):
		self.pin = led_pin
	def send(self,application,command):
		call(["irsend SEND_ONCE %s %s" % (str(application),str(command))],shell=True)

	#need  to create lirc config file
	#exambple : os.system("irsend SEND_ONCE samsungTV KEY_VOLUMEUP")
	#http://www.instructables.com/id/How-To-Useemulate-remotes-with-Arduino-and-Raspber/?ALLSTEPS