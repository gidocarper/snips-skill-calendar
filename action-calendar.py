#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from hermes_python.hermes import Hermes, MqttOptions
import configparser
import io
from musicplayer import MuuzikPlayer
import toml

USERNAME_INTENTS = "mcitar"
MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None


def add_prefix(intent_name):
    return USERNAME_INTENTS + ":" + intent_name

def read_configuration_file():
    try:
        cp = configparser.ConfigParser()
        with io.open("config.ini", encoding="utf-8") as f:
            cp.read_file(f)
        return {section: {option_name: option for option_name, option in cp.items(section)}
                for section in cp.sections()}
    except (IOError, configparser.Error):
        return dict()

def intent_callback_makeMeeting(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, "Termin erstellen")

def intent_callback_getMeeting(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, "Termin abrufen")

def intent_callback_deleteMeeting(hermes, intent_message):
    hermes.publish_end_session(intent_message.session_id, "Termin Löschen")


if __name__ == "__main__":
    config = read_configuration_file()
    musicplayer = MuuzikPlayer(config)

    snips_config = toml.load('/etc/snips.toml')
    if 'mqtt' in snips_config['snips-common'].keys():
        MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
    if 'mqtt_username' in snips_config['snips-common'].keys():
        MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
    if 'mqtt_password' in snips_config['snips-common'].keys():
        MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']
    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)

    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent('mcitar:makeMeeting', intent_callback_makeMeeting) \
            .subscribe_intent('mcitar:getMeeting', intent_callback_getMeeting) \
            .subscribe_intent('mcitar:deleteMeeting', intent_callback_deleteMeeting) \
            .loop_forever()
