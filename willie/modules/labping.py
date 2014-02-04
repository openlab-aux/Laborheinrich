# -*- coding: utf8 -*-

from __future__ import unicode_literals
import serial

"""

the labping module for OpenLab Augsburg

"""
from willie.module import commands


serial_dev = None
ltime = 5

def re_connect():
    global serial_dev
    

    try:
        serial_dev.close() # close an existing connection
    except:
        pass

    try:
        serial_dev = serial.Serial('/dev/lights', 9600, timeout=1)
    except:
        raise Exception('fatal: rundumleuchte connected?')


def setup(bot):
    re_connect()


@commands('labping')
def ping_openlab(bot, trigger):
    """
    heinrich lässt die Rundumleuchte im OpeLab aufleuchten
    """

    global ltime

    try:
        serial_dev.write(str(ltime))
    except serial.SerialException:
        bot.say(trigger.nick + ': Keine Verbindung zur Rundumleuchte :( Versuche es nochmal.')
        re_connect()
        return

    bot.say('Rundumleuchte wurde für ' + str(ltime) + ' Sekunden aktiviert')
