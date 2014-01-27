# -*- coding: utf8 -*-
"""

the labping module for OpenLab Augsburg

"""
from willie.module import commands


@commands('.labping')
def ping_openlab(bot, trigger):
    """
    heinrich lässt die Rundumleuchte im OpeLab aufleuchten
    """
    #rundumleuchte aktivieren
    sleep(5)
    #rundumleuchte deaktivieren


