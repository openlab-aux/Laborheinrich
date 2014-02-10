# -*- coding: utf8 -*-

"""
Twitter module for Heinrich
"""

from __future__ import unicode_literals

from willie.module import commands

from twython import Twython

class Twitter:
    api = None

def setup(bot):
    if bot.config.has_option('twitter', 'app_key') and bot.config.has_option('twitter', 'app_secret') and bot.config.has_option('twitter', 'oauth_token') and bot.config.has_option('twitter', 'oauth_token_secret'):
        Twitter.api = Twython(bot.config.twitter.app_key,
                              bot.config.twitter.app_secret,
                              bot.config.twitter.oauth_token,
                              bot.config.twitter.oauth_token_secret)

    else:
        raise Exception('twitter module not configured')


@commands('tweet')
def post(bot, trigger):
    if trigger.admin:
        tweet = " ".join(trigger.args[1].split(" ")[1:])
        Twitter.api.update_status(status=tweet)
        bot.say("Posted quote \"%s\" to @OpenLabAugsburg (http://twitter.com/OpenLabAugsburg)" % tweet)
    else:
        bot.say("Nope, you're not allowed to post.")
