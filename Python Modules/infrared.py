from subprocess import call

class Infrared():
	def __init__(self,led_pin):
		self.pin = led_pin
	def send(self,application,command,times):
		if command == "power":
			command = "KEY_POWER"
		elif command == "input_computer":
			command = "KEY_PC"
		elif command == "volume_up":
			command = "KEY_VOLUMEUP"
		for i in range(times):
			call(["irsend SEND_ONCE %s %s" % (str(application),str(command))],shell=True)

	#need  to create lirc config file
	#exambple : os.system("irsend SEND_ONCE samsungTV KEY_VOLUMEUP")
	#http://www.instructables.com/id/How-To-Useemulate-remotes-with-Arduino-and-Raspber/?ALLSTEPS