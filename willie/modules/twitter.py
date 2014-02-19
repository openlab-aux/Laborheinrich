# -*- coding: utf8 -*-

"""
Twitter module for Heinrich
"""

from __future__ import unicode_literals

from willie.module import commands
import re
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
        raise willie.config.ConfigurationError('twitter module not configured')


def tweet_len(tweet):
    # returns the lenght of a tweet while taking unter account
    # that each link counts 22 charakters

    tweet_len = len(tweet)
    links = re.findall(r'http[s]?://[\S]*', tweet) # extract all links

    for link in links:
        tweet_len -= len(link)
        tweet_len += 22

    return tweet_len


@commands('tweet')
def post(bot, trigger):

    length = 0

    if trigger.admin:
        tweet = trigger.group(2).strip()
        length = tweet_len(tweet)

        if length <= 140:
            Twitter.api.update_status(status=tweet)
            bot.say("Posted quote \"%s\" to @OpenLabAugsburg (http://twitter.com/OpenLabAugsburg)" % tweet)
        else:
            bot.say("Sorry, tweet is " + str(length - 140) + " charakters too long :(")
    else:
        bot.say("Nope, you're not allowed to post.")
