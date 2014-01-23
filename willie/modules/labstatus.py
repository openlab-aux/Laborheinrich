# -*- coding: utf8 -*-
"""

the labstatus module for OpenLab Augsburg

"""
from willie.module import commands, example
import urllib
import json


def is_lab_open():

    http_obj = urllib.urlopen('http://api.openlab-augsburg.de/data.json')
    json_data = http_obj.read()
    
    values = json.loads(json_data)

    http_obj.close()

    return values['open']


@commands('status')
#@example('.status')
def print_status(bot, trigger):
    """
    heinrich sagt dir, ob das OpenLab geoeffnet ist
    """
    if( is_lab_open() ):
        bot.say("Lab-Status: geoeffnet!")
    else:
        bot.say("Lab-Status: geschlossen :(")


