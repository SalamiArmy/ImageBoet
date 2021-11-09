# coding=utf-8
import sys
import main
reload(sys)
sys.setdefaultencoding('utf8')
import json
gettweet = main.get_platform_command_code('telegram', 'gettweet')
    
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).replace(bot.name, "").strip()
    if (requestText == ""):
        bot.sendMessage(chat_id=chat_id, text='Set Twitter bearer token like this:\n/settweet AAAAAAAAAAAAAAAAAAAAAFlUwQAAAAAAct%2B... etc.\nSee https://developer.twitter.com/en/docs/basics/authentication/oauth-2-0/bearer-tokens' + requestText)
    else:
        gettweet.setTwitterToken(chat_id, requestText)
        bot.sendMessage(chat_id=chat_id, text='Twitter token set to:' + requestText)
