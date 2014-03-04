# -*- coding: utf8 -*-

"""

the labping module for OpenLab Augsburg

"""

from __future__ import unicode_literals

import serial
from willie.module import commands
from willie.modules import flipdot_scroll_text
from willie.config import ConfigurationError


class Rundumleuchte:

    _serial_dev = None
    _dev_file = ''

    @staticmethod
    def connect(dev_file):
        try:
            Rundumleuchte._serial_dev = serial.Serial(dev_file, 9600, timeout=1)
            Rundumleuchte.dev_file = dev_file
        except:
            raise Exception('error: Rundumleuchte connected?')

    @staticmethod
    def re_connect():
        try:
            # close an existing connection before
            # trying to reconnect
            Rundumleuchte._serial_dev.close()
        except:
            pass

        Rundumleuchte.connect(Rundumleuchte.dev_file)

    @staticmethod
    def light_up():
        try:
            Rundumleuchte._serial_dev.write(str(Rundumleuchte.lightup_interval))
        except serial.SerialException, ValueError:
            return False

        return True


def setup(bot):
    if bot.config.has_option('rundumleuchte', 'device'):

        Rundumleuchte.connect(bot.config.rundumleuchte.device)

        if bot.config.has_option('rundumleuchte', 'lightup_interval'):
            Rundumleuchte.lightup_interval = bot.config.rundumleuchte.lightup_interval
        else:
            Rundumleuchte.lightup_interval = 5
    else:
        raise ConfigurationError('labping module not configured')


@commands('labping', 'pinglab')
def labping(bot, trigger):
    """
    heinrich lässt die Rundumleuchte im OpeLab aufleuchten
    """
    # do it twice if first try fails
    for i in range(2):
        if Rundumleuchte.light_up():
            bot.say('Rundumleuchte wurde für ' + str(Rundumleuchte.lightup_interval) + ' Sekunden aktiviert!')
            return
        if i == 0:
            bot.say(trigger.nick + ': Konnte Rundumleuchte nicht aktivieren, ich versuch´s noch einmal...')
            Rundumleuchte.re_connect()
        else:
            bot.say(trigger.nick + ': Nein, nichts zu machen :(')

    flipdot_scroll_text.scroll_text(trigger.group(2).strip())
