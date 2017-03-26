from vncdotool import api
import sys
import random
import json
import os
#from threading import Timer



def music(time,mood): #uses spotify window
    dir = os.path.join(sys.path[0], 'music.json')
    print (dir)
    with open(dir) as data_file:    
        music_all = json.load(data_file)
        music = []
    if time == "morning":
        music.extend(music_all["morning"])
    elif time == "night":
        music.extend(music_all["night"])
    if mood == "romance":
        music.extend(music_all["romance"])
    elif mood == "chill":
        music.extend(music_all["chill"])
    playlist = random.sample(music,1).pop()
    for i in range(len(music)):
        print music[i]
    client.mouseMove(320,1050)
    client.pause(3)
    client.mousePress(1)
    client.pause(2)
    client.keyPress('super-up')
    client.pause(1)
    client.keyPress('lctrl-l')
    client.pause(0.5)
    for i in playlist:
        client.keyPress(i)
    client.pause(0.5)
    client.keyPress('enter')
    client.pause(2.5)
    client.mouseMove(520, 320)
    client.pause(1)
    client.mousePress(1)
    for i in range(2):
        client.keyPress('lctrl-l')
        client.pause(0.5)

def log_in(dummy1, dummy2):
    #must wait 30-40 sec for pc to boot
    # for i in range(2):
    client.keyPress('enter')
    client.pause(1)
    for i in "1556":
        client.keyPress(i)
    #must wait at least 10 sec for pc to log in

def turn_off(dummy1, dummy2):
    
    client.pause(1)
    client.keyPress('ctrl-alt-del')
    client.pause(1)
    client.mouseMove(1860,1020)
    client.mousePress(1)
    client.pause(0.5)
    client.mouseMove(1860,960)
    client.mousePress(1)
    client.pause(1)
if __name__ == '__main__':
    client = api.connect("192.168.1.20")
    option = {"log_in":log_in, "turn_off":turn_off, "music":music}
    option[sys.argv[1]](sys.argv[2], sys.argv[3])
    sys.exit()