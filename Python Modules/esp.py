import requests

LEFT_LIGHT_PIN = 1
RIGHT_LIGHT_PIN = 2
TV_HIFI_PIN = 3


class Api():

	def __init__(self,address):
		self.address = address 
		resp = requests.get(self.address)
		if resp.status_code != 200:
			print("can't get status from api")

	def get_status(self,function,pin):
		resp = requests.get(self.address + "/" + function + "/" + pin)
		if resp.status_code !=200:
			print("can't get status from api: "+self.address+function+pin)
		answer = resp.json()
		return int(answer["id"]) #json data is string, "1"--> int 1 --> true/false
	
	def set_status(self,function,pin,status):
		if pin == "left_light":
			pin = LEFT_LIGHT_PIN
		elif pin == "tv-hifi":
			pin = TV_HIFI_PIN
		elif pin == "right_light":
			pin = RIGHT_LIGHT_PIN
		resp = requests.get(self.address + "/" + function + "/" + pin + "/" + status)

	def turn_on_pc(self):
		resp = requests.post(self.address + "/" + pc_on + "?params=0")

		