import sys
sys.path.insert(0, '/home/pi/glados_interface/python')
import esp
ESP8266_ADDRESS = "http://192.168.1.30"


ap = esp.Api(ESP8266_ADDRESS)
ap.set_status("digital", "tv-hifi", 1)