# -*- coding: utf8 -*-

"""
tumblr module for heinrich
"""

from __future__ import unicode_literals
from willie.module import commands
from pytumblr import TumblrRestClient

class Tumblr:
    api = None

def setup(bot):
    if bot.config.has_option('tumblr', 'consumer_key') and bot.config.has_option('tumblr', 'consumer_secret') and bot.config.has_option('tumblr', 'oauth_token') and bot.config.has_option('tumblr', 'oauth_secret'):
        Tumblr.api = TumblrRestClient(bot.config.tumblr.consumer_key,
                                      bot.config.tumblr.consumer_secret,
                                      bot.config.tumblr.oauth_token,
                                      bot.config.tumblr.oauth_secret)

    else:
        raise Exception('tumblr module not configured')


@commands('shit')
def post(bot, trigger):
    """
    heinrich posts shit as a quote directly to http://shitopenlabsays.tumblr.com
    """
    if trigger.admin:
        quote = trigger.group(2).strip()
        Tumblr.api.create_quote('shitopenlabsays',
                                type="quote",
                                quote=quote.decode('utf-8')
        bot.say("Posted quote \"%s\" to http://shitopenlabsays.tumblr.com" % quote)
    else:
        bot.say("Nope, you're not allowed to post.")

