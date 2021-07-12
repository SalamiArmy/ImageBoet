# coding=utf-8
import sys
import logging

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
        bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                        ', no token set. Try sending a valid twitter token with /settweet.')
    else:
        fetch_url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + requestText.replace(" ", "%20")
        raw_data = urlfetch.fetch(url=fetch_url,
                                  headers={'Authorization': 'Bearer ' + getToken}).content
        try:
            data = json.loads(raw_data)
            if ('errors' in data and len (data['errors']) > 0):
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                ',\n' + data['errors'][0]['message'].replace('.', ':') + 
                                ('\n' + getToken + '\nTry sending a valid twitter token with /settweet.' if data['errors'][0]['message']=='Invalid or expired token.' else ''))
            else:
                if ('statuses' in data and len(data['statuses']) > 0):
                    bot.sendMessage(chat_id=chat_id, text='\"' + data['statuses'][0]['text'] + '\" - ' + data['statuses'][0]['user']['name'] + '\n' + 
                                    str(data['statuses'][0]['retweet_count']) + ' retweets\n' + 
                                    'https://twitter.com/' + data['statuses'][0]['user']['screen_name'] + '/status/' + data['statuses'][0]['id_str'])
                    if ('retweeted_status' in data['statuses'][0]):
                        raw_data = urlfetch.fetch(url='https://api.twitter.com/1.1/statuses/show.json?id=' + data['statuses'][0]['retweeted_status']['id_str'],
                                                  headers={'Authorization': 'Bearer ' + getToken}).content
                        retweet_data = json.loads(raw_data)
                        logging.info('found some retweet data: ' + str(retweet_data))
                    return True
                else:
                    bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                    ', I\'m afraid I can\'t find any Twitter Tweets for ' +
                                    requestText)
        except ValueError:
            if (raw_data != ""):
                bot.sendMessage(chat_id=chat_id, text=raw_data)
            else:
                bot.sendMessage(chat_id=chat_id, text='twitter api url returned nothing: ' + fetch_url)
    return False
