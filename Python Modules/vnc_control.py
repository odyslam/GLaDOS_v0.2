import vncdotool
import sys



def vnc(function):

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

	vnc(music)
def log_in(dummy1,dummy2,dummy3):
	pass

def shutdown(dummy1,dummy2,dummy3):
	pass



if __name__ == '__main__':
	option = {"log_in":log_in, "turn_off":turn_off,"music":music}
	
	option[sys.argv[1]](sys.argv[2],sys.argv[3])