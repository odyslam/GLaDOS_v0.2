import pi_switch
import sys


#pin socket function

socket_on = ("000000010100010001010101","000000010101000001010101","000000010001010001010101")
socket_off = ("000000010100010001010100","000000010101000001010100","000000010001010001010100")
sender = pi_switch.RCSwitchSender()
sender.enableTransmit(int(sys.argv[1]))

def send(function,socket_number):
	if function == "1":
		sender.send(socket_on[socket_number-1])
	elif function == "0":
		sender.send(socket_off[socket_number-1])
	return 0



if __name__ == '__main__':
	send(sys.argv[2],int(sys.argv[3]))