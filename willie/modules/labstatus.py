# -*- coding: utf8 -*-
"""

the labstatus module for OpenLab Augsburg

"""
import willie.module
from willie.module import commands
import urllib
import json
import time
import thread

api_url = 'http://api.openlab-augsburg.de/data.json'
#api_url = 'http://files.michiwend.com/fakeapi/data.json'

def lab_is_open():

    http_obj = urllib.urlopen(api_url)
    json_data = http_obj.read()
    
    values = json.loads(json_data)

    http_obj.close()

    return values['open']



lab_was_open = lab_is_open()
@willie.module.interval(10)
def lurk(bot):
    
    global lab_was_open
         
    for channel in bot.channels:

        if( lab_is_open() and not lab_was_open ):
            bot.msg(channel, 'NEUER LAB-STATUS: geoeffnet!')
        elif ( not lab_is_open() and lab_was_open ):
            bot.msg(channel, 'NEUER LAB-STATUS: geschlossen.')
        
    lab_was_open = lab_is_open()
        


@commands('status')
def print_status(bot, trigger):
    """
    heinrich sagt dir, ob das OpenLab geoeffnet ist
    """
    if( lab_is_open() ):
        bot.say("Lab-Status: geoeffnet!")
    else:
        bot.say("Lab-Status: geschlossen.")


