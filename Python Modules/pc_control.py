# from vncdotool import api
import os

class Pc():
	def __init__(self,hostname):
		self.hostname = hostname
		

	def status(self):
		response = os.system("ping -c 1 " + self.hostname)
		if response !=0:
			return 0
		else:
			return 1

	def log_in(self):
		pass #call python2 script args log_int

	def turn_off(self):
		pass  #call python2 scripts args logg_off

	def music(self,time,mood): #time(morning,day,night), mood(chill_house,chill_acoustic,romanctic,energy,jazz,rock)
		if time == "morning":
			#call python2 scripts args: music time mood
			pass
		elif time == "enter_home":
			pass


	