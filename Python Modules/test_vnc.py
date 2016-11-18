import sys

sys.path.insert(0, '/home/pi/glados_interface/python')
import pc_control

PC_ADDRESS = "192.168.1.20"



pc = pc_control.Pc(PC_ADDRESS)

pc.vnc_control("log_in",0,0)