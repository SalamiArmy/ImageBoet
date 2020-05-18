
# coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import json
gettweet = main.get_platform_command_code('telegram', 'gettweet')
    
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
  requestText = str(message).replace(bot.name, "").strip()
  gettweet.setTwitterToken(chat_id, requestText)
