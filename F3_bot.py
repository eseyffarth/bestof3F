#!/usr/bin/python
# -*- coding: utf-8 -*-

owner = "ojahnn"        # Name des Accounts, an den Fehlermeldungen gesendet werden
import F3_config
import tweepy
import re
import random
import urllib2

def login():
    # for info on the tweepy module, see http://tweepy.readthedocs.org/en/

    # Authentication is taken from F3_config.py
    consumer_key = F3_config.consumer_key
    consumer_secret = F3_config.consumer_secret
    access_token = F3_config.access_token
    access_token_secret = F3_config.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api

def stick_together_output():
    bestseller_pages = ["http://www.spiegel.de/kultur/literatur/spiegel-bestseller-paperback-a-1025444.html",
                        "http://www.spiegel.de/kultur/literatur/spiegel-bestseller-taschenbuecher-a-1025518.html",
                        "http://www.spiegel.de/kultur/literatur/spiegel-bestseller-kinder-und-jugendbuecher-a-1025519.html",
                        "http://www.spiegel.de/kultur/literatur/spiegel-bestseller-hoerbuecher-a-1025528.html",
                        "http://www.spiegel.de/kultur/literatur/spiegel-bestseller-hardcover-a-1025428.html"]

    titel_RE = re.compile('<span class="title bestseller-popup-link">([^<]+)</span>')

    folgen = set()

    for bestseller_page in bestseller_pages:
        bestseller_content = urllib2.urlopen(bestseller_page)
        bestseller_content = bestseller_content.read()
        bestseller_content = bestseller_content.decode("latin-1")

        poss_titles = re.findall(titel_RE, bestseller_content)
        for poss_t in poss_titles:
            m = re.search("(^(Der|Die|Das|Mein|Unser|Ihr|Dein|Ein|Zwei|Drei|Vier|Fünf|Sechs|Sieben|Acht|Neun|Zehn)[^\:\.]+)", poss_t)
            if m:
                folgen.add(m.group(0)[0].lower() + m.group(0)[1:])

    folge = random.sample(folgen, 1)
    output = "Die drei Fragezeichen und "+folge[0]

    return output

def tweet_something(debug):
    api = login()
    output = stick_together_output()
    if debug:
        print(output)
    else:
        api.update_status(status=output)
        print(output)

tweeted = False
while not tweeted:
    try:
        tweet_something(False)
        tweeted = True
    except:
        pass
