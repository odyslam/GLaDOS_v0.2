# -*- coding: utf-8-*-
import random
import re
import request
WORDS = ["OPEN","DOOR"]
address = "127.0.0.1/macros/door/1"


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    try:
        req = requests.post(address, timeout=1)
    except requests.exceptions.RequestException as e:
        print ("error: " + str(e))

def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\bopen door\b', text, re.IGNORECASE))
