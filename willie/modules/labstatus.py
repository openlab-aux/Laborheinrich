# -*- coding: utf-8 -*-
"""

the labstatus module for OpenLab Augsburg

"""
from __future__ import unicode_literals

import willie.module
from willie.module import commands
import urllib
import json


# default values if nothing is configured
API_URL = 'http://api.openlab-augsburg.de/data.json'
INTERVAL = 10


def setup(bot):

    if bot.config.has_option('labstatus', 'api_url'):
        global API_URL
        API_URL = bot.config.labstatus.api_url

    if bot.config.has_option('labstatus', 'update_interval'):
        global INTERVAL
        INTERVAL = bot.config.labstatus.interval


class LabAPIHandler:

    def __init__(self, url):
        self.__url = url

    def update_data(self):
        http_obj = urllib.urlopen(self.__url)
        json_data = http_obj.read()
        self.__values = json.loads(json_data)
        http_obj.close()

    def get_lab_state(self):
        return self.__values['open']

    def get_active_clients(self):
        clients_value = self.__values['status'].split()[0]

        if( not clients_value.isnumeric() ):
            return 0
        else:
            return int(clients_value)


lab_was_open = False
@willie.module.interval(INTERVAL)
def lurk(bot):

    global lab_was_open
    global API_URL

    handler = LabAPIHandler(API_URL)
    handler.update_data()

    lab_is_open = handler.get_lab_state()

    for channel in bot.channels:

        if( lab_is_open and not lab_was_open ):
            bot.msg(channel, 'NEUER LAB-STATUS: geöffnet!')
        elif ( not lab_is_open and lab_was_open ):
            bot.msg(channel, 'NEUER LAB-STATUS: geschlossen.')

    lab_was_open = lab_is_open


@commands('status')
def print_status(bot, trigger):
    """
    heinrich sagt dir, ob das OpenLab geöffnet ist
    """

    global API_URL

    handler = LabAPIHandler(API_URL)
    handler.update_data()

    if( handler.get_lab_state() ):
        bot.say("Lab-Status: geöffnet. | aktive Geräte: " + `handler.get_active_clients()` )
    else:
        bot.say("Lab-Status: geschlossen.")
