from vncdotool import api
import sys
import random



def music(time,mood):
	music = []
	if time == "morning":
		music.append("morning acoustic")

	elif time == "night":
		music.append("late night jazz")
		music.append("spotify:user:spotify:playlist:4RmINrqBZGFs4NGTEWkeuT")

	if mood == "chill":
		music.append("spotify:user:11141301673:playlist:58x34vXnrK8YQQAvkqpqRB")
		music.append("spotify:user:spotify:playlist:3J3mTk0N0NzDOFgnp67Z75")
	if mood == "romance"
		music.append("spotify:user:11141301673:playlist:6xfhIWSeRW24HJfHvWaiGM")

	playlist = random.sample(music,1).pop()

	client.mouseMove(320,1050)
	client.pause(0.5)
	client.keyPress('super-up')
	client.pause(0.4)
	client.keyPress('lctrl-l')
	client.pause(0.5)
	for i in playlist:
		client.keyPress(i)
	client.pause(0.3)
	client.keyPress('enter')
	client.pause(0.5)
	client.mouseMove(500,300)
	client.mousePress(1)
	for i in range(2): 
		client.keyPress('lctrl-l')
		client.pause(0.5)

def log_in(dummy1,dummy2):
	#must wait 30-40 sec for pc to boot
	client.keyPress('enter')
	client.pause(0.5)
	for i in "1556":
		client.keyPress(i)
	#must wait at least 10 sec for pc to log in 

def shutdown(dummy1,dummy2):
	client.keyPress('ctrl-alt-del')
	client.mouseMove(1860,1020)
	client.mousePress(1)
	client.pause(0.5)
	client.mouseMove(1860,960)
	client.mousePress(1)

	#client.mouseMove(20,1060)
	#client.mousePress(1)
	#client.pause(0.5)
	#client.mouseMove(20,980)
	#client.mousePress(1)
	#client.pause(0.5)
	#client.mouseMove(100,910)
	#client.mousePress(1)



if __name__ == '__main__':
	
	client = api.connect("192.168.1.20")
	option = {"log_in":log_in, "turn_off":turn_off,"music":music}
	option[sys.argv[1]](sys.argv[2],sys.argv[3])