#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import time
from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

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

    def askjeedomInteractions_callback(self, hermes, intent_message):
        # terminate the session first if not continue

        print "Lancement de l'application jeedomInteractions"
        hermes.publish_end_session(intent_message.session_id, "")

        jeedomInteraction = None
   
        print '[Recep] intent value: {}'.format(intent_message.slots.Interaction.first().value)

        #if intent_message.slots.TvChannel.first().value == 'oncle':
            #print '[Received] intent: {}'.format(intent_message.slots.TvChannel)
        jeedomInteraction = intent_message.slots.Interaction.first().value
        #subcommandeFreebox = intent_message.slots.TvSubCommand.first().value

        if jeedomInteraction is None:
           Interaction_msg = "Interaction inexistante"
        #else:

        jeedomAPIKEY = self.config.get("secret").get("jeedomAPIKEY")
        jeedomIP = self.config.get("secret").get("jeedomIP")


        self.callInteraction(jeedomAPIKEY,jeedomIP)
    def callInteraction(self,jeedomIP,jeedomAPIKEY):
        requests.get('http://'+jeedomIP+'/core/api/jeeApi.php?apikey='+jedoomAPIKEY+'&type=interact&query='+jeedomInteraction)
#http://#IP_JEEDOM#/core/api/jeeApi.php?apikey='+jedoomAPIKEY+&type=interact&query=#QUERY#

    # --> Master callback function, triggered everytime an intent is recognized
    def jeedomInteraction_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name

        print '[Recept] intent {}'.format(coming_intent)
       #if coming_intent == 'Tarlak:ChannelFreebox':
            self.jeedomInteraction_callback(hermes, intent_message)
        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.jeedomInteraction_callback).start()

            print "jeedom Interaction"
if __name__ == "__main__":
    jeedomInteraction()
