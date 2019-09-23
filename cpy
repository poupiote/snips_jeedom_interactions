#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import requests
import time
from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
jeedomIP=None
jeedomAPIKEY=None
CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class jeedomInteraction(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()

        
    # --> Sub callback function, one per intent
    def interaction_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        jeedomAPIKEY = self.config.get("secret").get("jeedomAPIKEY")
        jeedomIP = self.config.get("secret").get("jeedomIP")        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        #jeedomInteraction = intent_message.slots.interaction.first().value
        requests.get('http://'+jeedomIP+'/core/api/jeeApi.php?apikey='+jeedomAPIKEY+'&type=interact&query='+jeedomInteraction)
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "Action1 has been done", "")    
    
    
    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'sscsieg:interactions':
            self.interaction_callback(hermes, intent_message)


        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    config = SnipsConfigParser.read_configuration_file("config.ini")
    jeedomIP = config.get("secret").get("jeedomIP")
    jeedomAPIKEY = config.get("secret").get("jeedomAPIKEY")
    print jeedomAPIKEY
    jeedomInteraction()
