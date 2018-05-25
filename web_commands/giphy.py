# coding=utf-8
import json
import random
import string
import urllib

import telegram


def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()

    giphyUrl = 'http://api.giphy.com/v1/gifs/search?q='
    apiKey = '&api_key=dc6zaTOxFJmzC&limit=10&offset=0'
    realUrl = giphyUrl + requestText + apiKey
    data = json.load(urllib.urlopen(realUrl))
    if data['pagination']['total_count'] >= 1:
        imagelink = data['data'][random.randint(0, len(data['data']) - 1)]['images']['original']['url']
        return str(imagelink)
    else:
        errorMsg = 'I\'m sorry Dave, I\'m afraid I can\'t find a giphy gif for ' + \
                   string.capwords(requestText.encode('utf-8')) + '.'
        return [errorMsg]
