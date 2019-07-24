# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import json

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

class TwitterToken(ndb.Model):
    # key name: chat_id
    twitterToken = ndb.StringProperty(indexed=False, default='')
    
def setTwitterToken(chat_id, token):
    es = TwitterToken.get_or_insert(str(chat_id))
    es.twitterToken = str(token)
    es.put()

def getTwitterToken(chat_id):
    es = TwitterToken.get_or_insert(str(chat_id))
    if es:
        return str(es.twitterToken)
    return ''
    
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
  requestText = str(message).replace(bot.name, "").strip()
  getToken = getTwitterToken(chat_id)
  if (getToken == ""):
    setTwitterToken(chat_id, requestText)
  else:
      raw_data = urlfetch.fetch(url='https://api.twitter.com/1.1/search/tweets.json?q=' + requestText,
                headers={'Authorization': 'Bearer ' + getToken})
      getContent = raw_data.content
      data = json.loads(getContent)
      if ('errors' in data and len (data['errors']) > 0):
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                              ',\n' + data['errors'][0]['message'].replace('.', ':') + 
            ('\n' + getToken + '\nTry sending a valid twitter token first.' if data['errors'][0]['message']=='Invalid or expired token.' else ''))
        setTwitterToken(chat_id, "")
      else:
          if ('statuses' in data and len(data['statuses']) > 0):
            bot.sendMessage(chat_id=chat_id, text=data['statuses'][0]['text'])
            return True
          else:
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                              ', I\'m afraid I can\'t find any Twitter Tweets for ' +
                                                              requestText)
      return False
