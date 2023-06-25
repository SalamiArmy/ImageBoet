# coding=utf-8
import json
import random
import string
import urllib

import telegram


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).replace(bot.name, "").strip()

    giphyUrl = 'http://api.giphy.com/v1/gifs/search?q='
    apiKey = '&api_key=dc6zaTOxFJmzC&limit=10&offset=0'
    realUrl = giphyUrl + requestText + apiKey
    data = json.load(urllib.urlopen(realUrl))
    bot.sendMessage(chat_id=chat_id, text=json.dumps(data))
