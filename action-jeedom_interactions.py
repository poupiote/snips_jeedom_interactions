#!/#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import request
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
from hermes_python.ontology.slot import *
import io
import time
import json

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    jeedomAPIKEY = self.config.get("secret").get("jeedomAPIKEY")
    jeedomIP = self.config.get("secret").get("jeedomIP")        
    # action code goes here...
    print '[Received] intent: {}'.format(intentMessage.intent.intent_name)
    jeedomInteraction = intentMessage.slots.interaction.first().value
    requests.get('http://'+jeedomIP+'/core/api/jeeApi.php?apikey='+jeedomAPIKEY+'&type=interact&query='+jeedomInteraction)
    # if need to speak the execution result by tts
    hermes.publish_start_session_notification(intentMessage.site_id, "Action1 a été exécutée", "")    
    #{{#each action_code as |a|}}{{a}}
    #{{/each}}


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("voleurdespace:interactions", subscribe_intent_callback) \
         .start()



