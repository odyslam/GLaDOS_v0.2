import httplib
import os
import subprocess
import logging
from datetime import datetime


# Script to be run by crontab every X minutes, probably ~5 is ideal.
class SystemRestart():

    def __init__(self,logfile): #use datetime module, once per day delete old file and make new one
        logging.basicConfig(filename= logfile,level=logging.INFO, format='%(asctime)s %(message)s')


    def have_internet(self):
        conn = httplib.HTTPConnection("www.google.com")
        try:
            conn.request("HEAD", "/")
            return True
        except:
            return False

    # Add mail client, when something is offline, send warning mail to owner or better send fb message! 


    def site_online(self):
        conn = httplib.HTTPConnection("192.168.1.19:8000")
        try:
            conn.request("HEAD", "/")
            return True
        except:
            return False


    def system_check(self): 
        hour = int(datetime.now().time().hour)
        if hour == 12:
            os.remove("/home/pi/glados_interface/python/system_monitor/sys.log")
        if self.have_internet() == False:
            logging.warning("No internet, rebooting Rooter")
            self.router_reboot() 
        elif self.site_online() == False:
            logging.warning("Interface is Down, rebooting Raspberry")
            os.system("sudo reboot")
        elif:
            logging.info("Everything are online, checking again in 5 min")


    def router_reboot(self):
        subprocess.call("python /home/pi/glados_interface/python/system_monitor/router_restart.py",shell = True)
        

if __name__ == '__main__':
    sr = SystemRestart( "/home/pi/glados_interface/python/system_monitor/sys.log")
    sr.system_check()