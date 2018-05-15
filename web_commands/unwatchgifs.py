# coding=utf-8
import main
unwatch = main.load_code_as_module('watchgifs').unwatch

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    unwatch(bot, chat_id)


