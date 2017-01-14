# -*- coding: utf-8 -*-

from threading import Timer

import logging
import logging.config
import os
import fbchat
import requests
from wit import Wit


class GladosBot(fbchat.Client):
    def __init__(self, email, password, debug=False, user_agent=None,log = False):
        fbchat.Client.__init__(self, email, password, debug, user_agent)
        self.authorised_names = ["odysseas lamtzidis"]
        self.conversations = {"odysseas lamtzidis": 0}  # ounts the individual conversations with the bot
        self.context = {}
        self.entities = {}
        self.log = log
        self.authorised_id = {}
        self.authorised_idrev = {}
        self.ip_address = "XYXYXYXYXYXYXYXY"
        self.authorised_update()
        self.send(self.authorised_id["odysseas lamtzidis"], "ETOIMOS")
        if log:
            self.logger("/home/pi/glados_interface/bot/conv.log")

        print ("listening...")

    def authorised_update(self):
        self.authorised_id.clear()
        self.authorised_idrev.clear()
        for name in self.authorised_names:
            self.authorised_id[name] = str(self.getUsers(name)[0].uid)
            self.authorised_idrev[self.authorised_id[name]] = name
            if name not in self.conversations:
                self.conversations[name] = 0

        Timer(30 * 60, self.authorised_update, []).start()

    def logger(self,logfile):
        logging.basicConfig(filename=logfile, level=logging.INFO, format='%(asctime)s %(message)s')
        logging.basicConfig(format='%(asctime)s %(message)s')

    def wit_start(self, token):
        actions = {
            'send': self.sendmessage,
            'heater': self.story_heater,
            'doors': self.story_doors,
            'hifi': self.story_hifi,
            'end': self.end,
            'authorise': self.story_authorise,
            'status': self.story_status
        }
        self.actions = actions
        self.wit = Wit(access_token=token, actions=actions)
        self.context = {}

    def first_entity_value(self, entities, entity):
        if entity not in entities:
            return None
        val = entities[entity][0]['value']
        if not val:
            return None
        return val['value'] if isinstance(val, dict) else val

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.author_id = str(author_id)
        self.markAsDelivered(author_id, mid)  # mark delivered
        self.markAsRead(author_id)
        self.message = message
        if self.log:
            logging.info("MESSAGE:" + str(message))
        if str(author_id) != str(self.uid):
            if str(author_id) not in str(self.authorised_id.values()):
                self.send(self.author_id, "Δεν έχεις άδεια επικοινωνίας, αποστέλω τα στοιχεία σου στον υπεύθηνο")
                self.send(self.authorised_id["odysseas lamtzidis"], "")
            else:
                print(str(author_id) + " <--author is ok, sending message to wit")
                if message == "sudo RESET":
                    self.end({})
                elif message == "sudo SHUTDOWN":
                    self.terminate()
                self.call_wit()
                # wit api-->message_analysis-->action

    def call_wit(self):
        self.auth_name = self.authorised_idrev[self.author_id] #author name
        self.conv_number = self.conversations[self.auth_name]
        self.session_id = str(self.authorised_idrev[self.author_id]) + '-number:' + str(self.conv_number)
        self.session_id = self.session_id.replace(" ", "-")
        print ("SESSION ID: " + str(self.session_id))
        self.context = self.wit.run_actions(self.session_id, self.message, self.context)
        if self.log:
            logging.info("Session ID:" + str(self.session_id))
            logging.info(self.context)
        print ("SELF.CONTEXT = " + str(self.context))

    def end(self, request):
        self.context.clear()
        self.conversations[self.auth_name] += 1
        print("--------------------------------END------------------------------------")
        if self.log:
            logging.info("-------------------------------------END------------------------------------------")
            logging.info(str(self.conversations))
        print(self.conversations)
        return self.context

    def sendmessage(self, request, response):
        if str(self.author_id) != str(self.uid):
            message = response['text']
            self.send(self.author_id, message)

    def macro_call(self, macro, args=None):
        print ("entered macro")
        url = self.ip_address + "/macros/" + macro + "/"
        if args:
            for i in range(len(args)):
                url += str(args[i])
                if not i == (len(args) - 1):
                    url += ","
        print (url)
        try:
            req = requests.post(url, timeout=1)
            try: 
                data = req.json()
                return data
            except:
                pass
        except requests.exceptions.RequestException as e:
            print ("error: " + str(e))
        print("macro call: " + str(macro) + " args")
        if self.log:
            logging.info("macro call: " + str(macro) + " args")

    def story_doors(self, request):
        self.context = request['context']
        self.entities = request['entities']
        print ("storry - doors")
        print(self.entities)
        intent = self.first_entity_value(self.entities, 'intent')
        sent = self.first_entity_value(self.entities, 'sentiment')
        door = self.first_entity_value(self.entities, 'doors')

        if not intent == "door_control":
            self.context.clear()
            self.context['uncertain'] = True
            return self.context
        if self.entities:
            for entity in self.entities:
                print ("entity is: " + str(entity))  # debug prints
                print (self.entities[entity][0])
                if self.entities[entity][0]['confidence'] < 0.8:
                    print ("confidence: " + str(self.entities[entity][0]['confidence']))
                    self.context.clear()                                # make sure that each entity has an acceptable
                    self.context['uncertain'] = True  # confidence value, otherway return "uncertain"
                    return self.context
            if not (sent or door):
                self.context['uncertain'] = True

        print ('perasa to loop')
        if self.context.get('uncertain') is not None:
            del self.context['uncertain']

        # act = self.first_entity_value(self.entities,'action') <--- irrelevant

        if sent == "positive":
            self.context['s_positive'] = True
        elif sent == "negative":  # sent = "negative"
            self.context['s_negative'] = True

        self.context[door] = True

        if door == "doors":
            self.macro_call("house", [1])
            self.context['2doors'] = True
        elif door == "door":
            self.macro_call("open_door", [1])
            self.context['1door'] = True
        else:
            self.context['uncertain'] = True
        print (self.context)
        return self.context

    def story_authorise(self, request):
        self.context = request['context']
        self.entities = request['entities']
        action = self.first_entity_value(self.entities, 'action')
        name = self.first_entity_value(self.entities, "authorised_name")
        if action == "authorise":
            self.authorised_names.append(name)
        elif action == "deauthorise":
            self.authorised_names.remove(name)
        self.authorised_update()
        return self.context

    def story_heater(self, request):
        self.context = request['context']
        self.entities = request['entities']
        print ("Heater - Entities: " + str(self.entities))

        intent = self.first_entity_value(self.entities, 'intent')

        # basic entities we are going to need for our story
        action = self.first_entity_value(self.entities, 'action')
        sent = self.first_entity_value(self.entities, 'sentiment')
        timetype = self.first_entity_value(self.entities, 'time_type')
        time = self.first_entity_value(self.entities, 'time_custom')
        heater = self.first_entity_value(self.entities, 'heater')

        if self.entities:
            for entity in self.entities:
                if str(entity) == "heater" and len(
                        self.entities[entity]) != 1:  # check if entity:"heater" has 2 values, boiler & bath
                    if self.entities[entity][1]['value'] == "bath":  # if it has, "bath" is standard time
                        time = 30
                        timetype = "minutes"
                print ("entity is: " + str(entity))  # debug prints
                print (self.entities[entity][0])

                if self.entities[entity][0]['confidence'] < 0.8:
                    print ("confidence: " + str(
                        self.entities[entity][0]['confidence']))  # make sure that each entity has an acceptable
                    self.context['uncertain'] = True  # confidence value, otherway return "uncertain"
                    return self.context

            if (intent != "heater_control" and heater != ("bath" and "boiler")) and (
            not 'no_ctime' in self.context):  # by checking for either bath or boiler entities, we double-check the certainty if the story
                self.context.clear()
                self.context['uncertain'] = True
                return self.context

            elif not (action or sent):
                self.context.clear()                                   # check if action or sent == None
                self.context['uncertain'] = True
                return self.context
        # if the code reaches here, there is no uncertainty and therefore we delete the uncertain-key 
        # (if it exists from a previous step of the conversation)

        if self.context.get('uncertain') is not None:
            del self.context['uncertain']

        if action == "close":  # if action is "closed", we don't need to continue with the rest of the function
            self.context['turn_off'] = True
            self.macro_call("heater", [0, 0])
            return self.context

        self.context[action] = action  # action is  "open"

        if sent == "positive":
            self.context['s_positive'] = True
        elif sent == "negative":
            self.context['s_negative'] = True

        if time and timetype and action:  # if boiler has all the needed - info, it proceeds to the action

            if self.context.get('no_ctime') is not None:  # we make sure that we delete all unecessary context
                del self.context['no_ctime']  # so as not to confuse our wit_bot

            self.context['ctime'] = str(time)

            time = int(time) * 60  # convert time to min
            if timetype == "minutes":
                self.context['timetype'] = "λεπτά"
            elif timetype == "hours":
                self.context['timetype'] = "ώρα"
                time *= 60
            self.macro_call("heater", [1, time])

        elif (not time) and (sent and action):  # apparently we have the action but not the time, we prompt wit to ask the user
            if self.context.get('time') is not None:  # we make sure that we delete all unecessary context 
                del self.context['ctime']  # so as not to confuse our wit_bot
            if self.context.get('timetype' is not None):
                del self.context['timetype']
            self.context['no_ctime'] = True
        print self.context
        return self.context

    def story_hifi(self, request):                  # Να φτιαξω την λουπα/ιστορια στο γουιτ, δεν ακολουθει
        self.context = request['context']           # την διαδρομη που πρεπει
        self.entities = request['entities']
        print("mpika hifi\n")
        print(self.entities)
        # sent = self.first_entity_value(self.entities, 'sentiment')
       
        action = self.first_entity_value(self.entities, 'action')
        amount = self.first_entity_value(self.entities, 'amount')
        hifi = self.first_entity_value(self.entities, 'hifi')
        intent = self.first_entity_value(self.entities, 'intent')
        continuance = self.first_entity_value(self.entities, 'continuance')

        if not (action or amount or hifi) and not continuance:
            self.context.clear()
            self.context['uncertain'] = True
            return self.context
        
        elif continuance == "stop":
            self.context.clear()
            self.context['stop'] = True
            return self.context

        if self.entities:
            for entity in self.entities:
                print ("enti"
                       "ty is: " + str(entity))  # debug prints
                print (self.entities[entity][0])
                if self.entities[entity][0]['confidence'] < 0.8:
                    print ("confidence: " + str(
                        self.entities[entity][0]['confidence']))
                    self.context.clear()                            # make sure that each entity has an acceptable
                    self.context['uncertain'] = True
                    return self.context  # confidence value, otherway return "uncertain"

                    # if sent == "positive":
                    #    self.context['s_positive'] = True
                    # else:
                    #   self.context['s_negative'] = True


        if hifi == "volume" or (self.context['action'] in ["increase","decrease"]): 
            if action:
                self.context['action'] = action  # decrease/increase
            if amount == "much":
                amount = 8
            elif amount == "little":
                amount = 3
            elif not amount:
                self.context["no_vol_amount"] = True
            if amount:
                self.context['vol_amount'] = amount
            if (action or self.context['action']) == "increase":
                self.context['vol_action'] = "δυναμώνω"
                self.macro_call("hifi", ["volume_up", self.context['vol_amount']])
            elif (action or self.context['action']) == "decrease":
                self.context['vol_action'] = "χαμηλώνω"
                self.macro_call("hifi", ["volume_down", self.context['vol_amount']])

        elif hifi == "general":
            if action == "open":
                self.context['switch'] = "Ανοίγω"
            elif action == "close":
                self.context['switch'] = "Κλείνω"
            self.macro_call("hifi", ["power"])

        if self.context.get('uncertain') is not None:
            del self.context['uncertain']

        return self.context

    def story_status(self,request):
        self.context = request['context']
        self.entities = request['entities']
        intent = self.first_entity_value(self.entities, 'intent')
        print ("status storry")
        if intent == "house_status":
            status_dict = self.macro_call("status",[]) #JSON dict object
            for appliance in ['l_light', 'r_light', 'o_light', 'he_status', 'pc_status']:
                if status_dict[appliance]:
                    self.context[appliance] = "Ανοικτό"
                else:
                    self.context[appliance] = "Κλειστό"
                if appliance in ['he_status', 'pc_status']:
                    self.context[appliance] += "ς"
            if status_dict['he_status']:
                self.context['el_timemin'] = status_dict['el_time'] / 60
                self.context['el_timesec'] = status_dict['el_time'] % 60
            else:
                self.context['el_timemin'] = self.context['el_timesec'] = 0

            if self.context.get('uncertain') is not None:
                del self.context['uncertain']

            print ("context is: " + str(self.context))

        else:
            self.context['uncertain'] = True

        assert isinstance(self.context, object)
        return self.context

    def terminate(self):
          os._exit(0)


if __name__ == '__main__': #change listen() so it returns 0 when an error occurs
    online = False
    while not online:
        try:
            bot = GladosBot ("XXXXXXXX", "YYYYYYYYY",log = False) #if the bot times-Out of fb, make a new session
        except:
            print ("error in starting bot,retrying.......")
            continue
        bot.wit_start("XYXYXYXYXYXYXYXY")
        online = bot.listen()
