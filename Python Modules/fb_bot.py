# -*- coding: utf-8 -*-

import fbchat
import requests
from wit import Wit
from threading import Timer

class GladosBot(fbchat.Client):

    def __init__(self,email, password,debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
        self.authorised_names = ["odysseas lamtzidis"]
        self.conversations = {"odysseas lamtzidis":1} #counts the individual conversations with the bot
        self.authorised_update()
        self.ip_address = "htttp://odys:defiler007@192.168.1.19:5000"

    def authorised_update(self):
        self.authorised_id = {}
        self.authorised_idrev = {}
        for name in self.authorised_names:
            self.authorised_id[name] = str(self.getUsers(name)[0].uid)
            self.authorised_idrev[self.authorised_id[name]] = name
            print self.authorised_id
            print self.authorised_idrev
            if not name in self.conversations:
                self.conversations[name] = 0

        Timer(30*60,self.authorised_update,[]).start()

    def wit_start(self,token):
        actions = {
            'send':  self.sendmessage,
            'heater':       self.story_heater,
            'doors' :       self.story_doors,
            'hifi'  :       self.story_hifi,
            'end'   :       self.end,
            'authorise':    self.story_authorise


        }
        self.actions = actions
        self.wit = Wit(access_token=token, actions=actions)
        self.context = {}
        
    def first_entity_value(self,entities, entity):
        if entity not in entities:
            return None
        val = entities[entity][0]['value']
        if not val:
            return None
        return val['value'] if isinstance(val, dict) else val
    
    def on_message(self, mid, author_id, author_name, message, metadata):
        self.author_id = str(author_id)
        self.markAsDelivered(author_id, mid) #mark delivered
        self.markAsRead(author_id) 
        self.message = message
       # print self.message
        self.author_name = author_name
        #print author_name
        if str(author_id) != str(self.uid):
            if str(author_id) not in str(self.authorised_id.values()):
                #print ("authid:"+ç str(author_id)+"kai value:" + str(self.authorised_id["odysseas lamtzidis"]))
                self.send(self.author_id,"Δεν έχεις άδεια επικοινωνίας, αποστέλω τα στοιχεία σου στον υπεύθηνο")
                #print self.author_id
                #print self.authorised_id["odysseas lamtzidis"]
                self.send(self.authorised_id["odysseas lamtzidis"],"lol")
            else:
                #print self.author_id
                #print self.authorised_id["odysseas lamtzidis"]
                self.call_wit()

            #wit api-->message_analysis-->action

    def call_wit(self):
        auth_name = self.authorised_idrev[self.author_id]
        conv_number = self.conversations[auth_name]
        self.session_id = str(self.authorised_idrev[self.author_id]) + '-number:' + str(conv_number)
        self.session_id = self.session_id.replace(" ","-")
        print self.session_id
        self.context = self.wit.run_actions(self.session_id,self.message, self.context)

    def end(self):
        self.context = {}
        self.conversations[self.author_name]+=1 
    
    def sendmessage(self,request,response):
        if str(self.author_id) != str(self.uid):
            message = response['text']
            self.send(self.author_id,message)

    def macro_call(self,macro,args = None):
       # url = self.ip_address + "/macros/" + macro + "/"
        #if args:
        #    for i in range(len(args)):
         #       url = url + str(args[i])
          #      if not i == (len(args)-1):
           #         url = url + ","

       # req=reuqests.post(url)
       return None

    def story_doors(self,request):
        self.context = request['context']
        self.entities = request['entities']

        act = self.first_entity_value(self.entities,'action')
        sent = self.first_entity_value(self.entities,'sentiment')
        door = str(self.first_entity_value(self.entities,'doors'))
        if sent == "positive":
            self.context['s_positive'] = True
        else:
            self.context['s_negative'] = True
        self.context[door] = True
        if door == "doors":
            self.macro_call("house",[1])
        elif door == "door":
            self.macro_call("open_door",[1])

        return self.context

    def story_authorise(self,request):
        self.context = request['context']
        self.entities = request['entities']
        action = self.first_entity_value(self.entities,'action')
        if action == "authorise":
            self.authorised_names.append(name)
        elif action == "deauthorise":
            self.authorised_names.remove(name)
        self.authorised_update()

        return self.context

    def story_heater(self,request):
        self.context = request['context']
        self.entities = request['entities']
        
        act = self.first_entity_value(self.entities,'action')
        sent = self.first_entity_value(self.entities,'sentiment')
        try:
            time = int(self.first_entity_value(self.entities,'time_custom'))
        except:
            time = None
        timetype = self.first_entity_value(self.entities,'time_type')
        if (time and timetype):
            self.context['ctime'] = str(time)
            if sent == "positive":
                self.context['s_positive'] = True
            else:
                self.context['s_negative'] = True
            if timetype == "hours":
                time = int(time) * 60
            self.macro_call("heater",[1,time])
        elif not time:
            print("notime")
            self.context['no_ctime'] = True
        return self.context
 
    def story_hifi(self,request):
        print hifi
            

bot = GladosBot("XXXXXXXX","XXXXXXX")
bot.wit_start("XXXXXXXXX")
bot.listen()
