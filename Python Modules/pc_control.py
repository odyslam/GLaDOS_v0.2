# from vncdotool import api
import os
import sys

class Pc():
	def __init__(self,hostname):
		self.hostname = hostname
		

	def status(self):
		response = os.system("ping -c 1 " + self.hostname)
		if response !=0:
			return 0
		else:
			return 1

	def vnc_control(self,function,time,mood): #function = log_in/shutdown/music + args
		subprocess.call("path/to/script %s %s %s" %(function,time,mood))

