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
    if data['pagination']['total_count'] >= 1:
        imagelink = data['data'][random.randint(0, len(data['data']) - 1)]['images']['original']['url']
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_DOCUMENT)
        bot.sendDocument(chat_id=chat_id,
                         filename=str(requestText) + '.gif',
                         document=str(imagelink))
        return str(imagelink)
    else:
        errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                   ', I\'m afraid I can\'t find a giphy gif for ' + \
                   string.capwords(requestText.encode('utf-8')) + '.'
        bot.sendMessage(chat_id=chat_id, text=errorMsg)
        return [errorMsg]