import httplib
import os
from threading import Timer
import subprocess

class SystemRestart():

    def __init__(self,interval):
        self.interval = interval
        Timer(interval*60,self.system_check).start()

    def have_internet(self):
        conn = httplib.HTTPConnection("www.google.com")
        try:
            conn.request("HEAD", "/")
            return True
        except:
            return False


    def site_online(self):
        conn = httplib.HTTPConnection("192.168.1.19:8000")
        try:
            conn.request("HEAD", "/")
            return True
        except:
            return False


    def system_check(self):
        if self.have_internet() == False:
            self.router_reboot() 
        elif self.site_online() == False:
             os.system("sudo reboot")
        else:
            Timer(self.interval*60,self.system_check).start()
    def router_reboot(self):
        subprocess.call("python /home/pi/glados_interface/python/router_restart.py",shell = True)
        


if __name__ == '__main__':
    sr = SystemRestart(10)