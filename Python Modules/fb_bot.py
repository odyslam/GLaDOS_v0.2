# -*- coding: utf-8 -*-

import fbchat
import requests
from wit import Wit
from threading import Timer

class GladosBot(fbchat.Client):

    def __init__(self,email, password,debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
        self.authorised_names = ["odysseas lamtzidis"]
        self.conversations = {"odysseas lamtzidis":0} #counts the individual conversations with the bot
        self.authorised_update()
        self.ip_address = "htttp://odys:defiler007@192.168.1.19:5000"

    def authorised_update(self):
        self.authorised_id = {}
        for name in self.authorised_names:
            self.authorised_id[name] = client.getUsers(name)[0].uid
            if not in self.conversations:
                self.conversations[name] = 0

        Timer(30*60,self.authorised_update,[]).start()

    def wit_start(self,token):
        self.actions = {
            'sendmessage':  self.sendmessage,
            'heater':       self.story_heater,
            'doors' :       self.story_doors,
            'hifi'  :       self.story_hifi,
            'end'   :       self.end,
            'authorise':    self.story_authorise


        }
        
        self.wit_token = token
        self.wit = Wit(access_token=self.wit_token, actions=self.actions)
        
    def first_entity_value(entities, entity):
        if entity not in entities:
            return None
        val = entities[entity][0]['value']
        if not val:
            return None
        return val['value'] if isinstance(val, dict) else val
    
    def on_message(self, mid, author_id, author_name, message, metadata):
        self.author_id = author_id
        self.markAsDelivered(author_id, mid) #mark delivered
        self.markAsRead(author_id) 
        self.message = message
        self.author_name = author_name
        if author_id not in self.authorised_id.values():
            self.send(self.author_id,"Δεν έχεις άδεια επικοινωνίας, αποστέλω τα στοιχεία σου στον υπεύθηνο")
            self.send(self.authorised_id["odysseas lamtzidis"],"ο " + str(self.author_name) + " μου έστειλε αυτό \"" + message + "\"")
        else:
            self.call_wit

            #wit api-->message_analysis-->action

    def call_wit(self):
        self.session_id = self.author_name + "-number:" + str(self.conversations[self.author_name])
        self.context = client.run_actions(self.session_id,self.message, self.context)

    def end(self):
        self.context = {}
        self.conversations[self.author_name]+=1 
    
    def sendmessage(self,request,response):
        if str(self.author_id) != str(self.uid):
            message = reponse['text']
            self.send(self.target_id,message)

    def macro_call(self,macro,args):
        if macro == "heater":
            if args[1] == "hours":
                args[0] = args[0] * 60
                args[0] = str(time)

        url = self.ip_address + "/macros/" + macro + "/"
        if args:
            for i in range(len(args)):
                url = url + str(args[i])
                if not i == (len(args)-1):
                    url = url + ","
         r=reuqests.post(url)

    
    def story_doors(self,request):
        self.context = request['context']
        self.entities = request['entities']

        act = first_entity_value(self.entities,'action')
        sent = first_entity_value(self.entities'sentiment')
        door = str(first_entity_value(self.entities'doors'))
        if sent == "positive"
            self.context['s_positive'] = True
        else:
            self.context['s_negative'] = True
        self.context[door] = True

        return self.context

    def story_authorise(self,request):
        self.context = request['context']
        self.entities = request['entities']
        action = first_entity_value(self.entities,'action')
        if action == "authorise":
            self.authorised_names.append(name)
        elif action == "deauthorise":
            self.authorised_names.remove(name)
        self.authorised_update()

        return self.context

    def story_heater(self,request):
        self.context = request['context']
        self.entities = request['entities']
        
        act = first_entity_value(self.entities,'action')
        sent = first_entity_value(self.entities,'sentiment')
        time = int(first_entity_value(self.entities,'time_custom'))
        timetype = first_entity_value(self.entities,'time_type')
        if (time && timetype):
            self.context('ctime') = str(time)
            if sent == "positive"
                self.context('s_positive') = True
            else:
                self.context('s_negative') = True
        elif not time:
            self.context('no_ctime') = True

        return self.context
 

            

bot = GladosBot("odyslam@icloud.com","glados007")
bot.wit_start("767CDEYBYRJPEXKHCO67LJPCFTKXKVQP")
bot.listen()