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

REMOTE_ADDR = 'http://hd1.freebox.fr/pub/remote_control?code='


class TelecommandeFreebox(object):
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

    def askFreeboxCommand_callback(self, hermes, intent_message):
        # terminate the session first if not continue

        print "Lancement de l'application Telecommandereebox"
        hermes.publish_end_session(intent_message.session_id, "")

        commandeFreebox = None
        subcommandeFreebox = None

        print '[Recep] intent value: {}'.format(intent_message.slots.TvCommand.first().value)

        #if intent_message.slots.TvChannel.first().value == 'oncle':
            #print '[Received] intent: {}'.format(intent_message.slots.TvChannel)
        commandeFreebox = intent_message.slots.TvCommand.first().value
        #subcommandeFreebox = intent_message.slots.TvSubCommand.first().value

        if commandeFreebox is None:
            telecommande_msg = "Je ne comprend pas ce que vous me demandez"
        #else:

        FREEREMOTECODE = self.config.get("secret").get("freeremotecode")


        print "Channel"
        if commandeFreebox == 'power':
            self.powerFreebox(FREEREMOTECODE)
        elif commandeFreebox == 'pip':
            self.pip(FREEREMOTECODE)
        elif commandeFreebox == 'switchpip':
            self.switchPip(FREEREMOTECODE)
        elif commandeFreebox == 'stopip':
            self.stopPip(FREEREMOTECODE)
        elif commandeFreebox == 'direct':
            self.direct(FREEREMOTECODE)
        elif commandeFreebox == 'rewind':
            self.rewind(FREEREMOTECODE)
        elif commandeFreebox == 'forward':
            self.forward(FREEREMOTECODE)
        elif (commandeFreebox == 'play') or (commandeFreebox == 'pause'):
            self.playPause(FREEREMOTECODE)
        elif (commandeFreebox == 'mute') or (commandeFreebox =='unmute'):
            self.muteUnmute(FREEREMOTECODE)
        elif commandeFreebox == 'volDown':
            self.volDown(FREEREMOTECODE)
        elif commandeFreebox == 'volup':
            self.volUp(FREEREMOTECODE)
        elif commandeFreebox == 'television' :
            self.television(FREEREMOTECODE)
        elif commandeFreebox=='twitch':
            self.twitch(FREEREMOTECODE)
        elif commandeFreebox == 'sortprogrammetv' :
            self.exitProgTv(FREEREMOTECODE)
        elif commandeFreebox == 'programmetv':
            self.progTv(FREEREMOTECODE)
        #elif (subcommandeFreebox is not None) and (subcommandeFreebox == 'chaîne'):
        #    if (commandeFreebox == 'next') :
        #        self.nextChannel(FREEREMOTECODE)
        #    elif (commandeFreebox== 'previous'):
        #        self.previousChannel(FREEREMOTECODE)
        elif (commandeFreebox == 'next'):
            self.right(FREEREMOTECODE)
        elif (commandeFreebox == 'previous') :
            selft.left(FREEREMOTECODE)
        else :
            self.channelChange(commandeFreebox,FREEREMOTECODE)

            #telecommande_msg = 'J\'allume la télévision'
        # if need to speak the execution result by tts
        #    hermes.publish_start_session_notification(intent_message.site_id, telecommande_msg, "FreeboxTelecommande")
        #
    def nextChannel(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=prgm_inc')

    def previousChannel(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=prgm_dec')

    def left(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=left')

    def right(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=right')

    def next(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&KEY=next')

    def previous(self,FREEREMOTECODE):
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&KEY=prev')

    def powerFreebox(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=power')
        #If a default channel is set the freebox zap on it
        DEFAULT_CHANNEL = self.config.get("secret").get("defaultchannel")
        DEFAULT_VOLUME = self.config.get("secret").get("defaultvolume")

        if DEFAULT_CHANNEL != None :
            time.sleep(18)
            # If a default value for the volum is set then the freebox volume go to zeor and
            # step by step up
            if DEFAULT_VOLUME != None:
                self.volDown(FREEREMOTECODE)
                self.volDown(FREEREMOTECODE)
                self.volDown(FREEREMOTECODE)
                self.volDown(FREEREMOTECODE)
                for i in range(0,int(DEFAULT_VOLUME)) :
                        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=vol_inc')
            self.television(FREEREMOTECODE)
            time.sleep(2)
            self.channelChange(DEFAULT_CHANNEL,FREEREMOTECODE)

    def switchPip(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=red')

    def stopPip(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=green')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=ok')

    def pip(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=yellow')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=yellow')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=right')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=ok')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=red')

    def direct(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=green')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=ok')

    def rewind(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=bwd&long=true')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=bwd&long=true')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=bwd&long=true')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=bwd&long=true')
        time.sleep(1)

    def forward(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=fwd&long=true')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=fwd&long=true')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=fwd&long=true')
        time.sleep(1)

    def playPause(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=play')

    def muteUnmute(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=mute')

    def volDown(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=vol_dec&long=true')

    def volUp(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=vol_inc&long=true')

    def television(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=home')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=home')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=ok')

    def exitProgTv(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=red')

    def progTv(self,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=home')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=home')
        time.sleep(2)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=ok')
        time.sleep(6)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=green')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=down')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=ok')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=ok')
        time.sleep(1)

    def twitch(selft,FREEREMOTECODE):
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=home')
        time.sleep(1)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=home')
        time.sleep(3)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=left')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=left')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=up')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=up')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=ok')
        time.sleep(4)
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=down')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=down')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=down')
        requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key=down')


    def channelChange(self,commandeFreebox,FREEREMOTECODE):
        time.sleep(1)
        for digit in commandeFreebox:
            requests.get(REMOTE_ADDR+FREEREMOTECODE+'&key='+digit)

    # --> Master callback function, triggered everytime an intent is recognized
    def FreeboxTelecommande_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name

        print '[Recept] intent {}'.format(coming_intent)
        if coming_intent == 'Tarlak:ChannelFreebox':
            self.askFreeboxCommand_callback(hermes, intent_message)
        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.FreeboxTelecommande_callback).start()

if __name__ == "__main__":
    TelecommandeFreebox()
