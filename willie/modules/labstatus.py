# coding: utf-8
"""

the labstatus module for OpenLab Augsburg

"""
import willie.module
from willie.module import commands
import urllib
import json
import time
import thread


API_URL = 'http://api.openlab-augsburg.de/data.json'
#API_URL = 'http://files.michiwend.com/fakeapi/data.json'


class LabAPIHandler:

    def update_data(self):

        global API_URL

        http_obj = urllib.urlopen(API_URL)
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


# check every 10 seconds if state has changed
lab_was_open = False
@willie.module.interval(10)
def lurk(bot):

    global lab_was_open

    handler = LabAPIHandler()
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
    heinrich sagt dir, ob das OpenLab geoeffnet ist
    """

    handler = LabAPIHandler()
    handler.update_data()

    if( handler.get_lab_state() ):
        bot.say("Lab-Status: geoeffnet. | aktive Geraete: " + `handler.get_active_clients()` )
    else:
        bot.say("Lab-Status: geschlossen.")
