# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import json

from google.appengine.api import urlfetch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
  requestText = str(message).replace(bot.name, "").strip()
  raw_data = urlfetch.fetch(url='https://api.twitter.com/1.1/search/tweets.json?q=' + requestText,
            headers={'Authorization': 'Bearer ' + keyConfig.get('Twitter', 'TOCKEN')})
  data = json.loads(raw_data.content)
  if ('statuses' in data and len(data['statuses']) > 0):
    bot.sendMessage(chat_id=chat_id, text=data['statuses'][0]['text'])
    return True
  else:
    bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find any Twitter Tweets for ' +
                                                      requestText)
    return False
