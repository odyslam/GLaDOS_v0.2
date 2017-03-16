# from vncdotool import api
import os
import subprocess

class Pc():
	def __init__(self,hostname):
		self.hostname = hostname
		

	def status(self):
		response = os.system("fping -c1 -t500 " + self.hostname)
		if response !=0:
			return 0
		else:
			return 1

	def vnc_control(self,function,time,mood): #function = log_in/shutdown/music + args
		subprocess.Popen("sudo python /home/pi/glados_interface/python/vnc_control.py %s %s %s" %(function,time,mood),shell=True)

