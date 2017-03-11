from subprocess import call

class Infrared():
	def __init__(self,led_pin):
		self.pin = led_pin
		self.power_status = 0
	def send(self, application, command, times):
		if command == "power":
			command = "KEY_POWER"
			self.power_status = 1 - self.power_status
		elif command == "input_computer":
			command = "KEY_PC"
		elif command == "volume_up":
			command = "KEY_VOLUMEUP"
		elif command == "volume_down":
			command  = "KEY_VOLUMEDOWN"
		for i in range(times):
			call(["irsend SEND_ONCE %s %s" % (str(application),str(command))],shell=True)

	#need  to create lirc config file
	#exambple : os.system("irsend SEND_ONCE samsungTV KEY_VOLUMEUP")
	#http://www.instructables.com/id/How-To-Useemulate-remotes-with-Arduino-and-Raspber/?ALLSTEPS