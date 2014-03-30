# -*- coding: utf-8 -*-

"""

the labstatus module for OpenLab Augsburg

"""

from __future__ import unicode_literals

import willie.module
from willie.module import commands
import urllib
import json
import time
import datetime
import string

LURK_INTERVAL = 10

def setup(bot):

    if not bot.config.has_option('labstatus', 'api_url') \
    or not bot.config.has_option('labstatus', 'topic_draft'):
        raise willie.config.ConfigurationError('labstatus module not configured')

    bot.memory['lab_was_open'] = False


class LabAPIHandler:

    def __init__(self, url):
        self.__url = url

    def update_data(self):
        try:
            http_obj = urllib.urlopen(self.__url)
            json_data = http_obj.read()
            self.__values = json.loads(json_data)
            http_obj.close()
            return True
        except IOError:
            return False

    def get_lab_state(self):
        try:
            return self.__values['open']
        except (ValueError, KeyError):
            return 'failed'
        ''' TODO:
            handle exceptions in functions '''

    def get_active_clients(self):
        try:
            clients_value = self.__values['status'].split()[0]

            if( not clients_value.isnumeric() ):
                return 0
            else:
                return int(clients_value)
        except (ValueError, KeyError):
            return -1

    def get_last_change(self):
        try:
            return self.__values['lastchange']
        except (ValueError, KeyError):
            return -1


def uptime(timestamp1, timestamp2):

    dtime   = int(timestamp2 - timestamp1)

    days    = int(dtime / 86400)
    rest    = dtime % 86400

    hours   = int(rest / 3600)
    rest    = rest % 3600

    minutes = int(rest / 60)
    seconds = rest % 60

    if days:
        tstring = str(days)
        if days>1:
            tstring += ' Tage, '
        else:
            tstring += ' Tag, '
    else:
        tstring = ''

    tstring += str(hours).zfill(2)+':'+str(minutes).zfill(2)+':'+str(seconds).zfill(2)

    return tstring


@willie.module.interval(LURK_INTERVAL)
def lurk(bot):

    print('lurink...')

    handler = LabAPIHandler(bot.config.labstatus.api_url)
    
    if handler.update_data():

        lab_is_open  = handler.get_lab_state()
        lab_was_open = bot.memory['lab_was_open']

        status_str = ''

        if( lab_is_open and not lab_was_open ):   # state changed to 'open'
            status_str = 'geöffnet!'
        elif( not lab_is_open and lab_was_open ): # state changed to 'closed'
            status_str = 'geschlossen.'
        else:                                     # nothing happend
            return

        topic = string.replace(bot.config.labstatus.topic_draft, '$STATUS', status_str)
        
        for channel in bot.channels:
            bot.write(('TOPIC', channel + ' :' + string.replace(topic, '$CHANNEL', channel)))
            bot.msg(channel, '+++ NEUER LAB-STATUS: ' + status_str + ' +++')

        bot.memory['lab_was_open'] = lab_is_open

    else:
        print('API call failed');


@commands('status')
def print_status(bot, trigger):
    """
    heinrich sagt dir, ob das OpenLab geöffnet ist
    """

    handler = LabAPIHandler(bot.config.labstatus.api_url)
    if handler.update_data():

        if( handler.get_lab_state() ):
            bot.say('Lab-Status: geöffnet. | aktive Geräte: ' + str(handler.get_active_clients())
                    )#+ ' | Geöffnet: ' + uptime(handler.get_last_change(), time.time()))
        else:
            bot.say('Lab-Status: geschlossen.')
        
    else:
        bot.say('API-Call nicht möglich')
