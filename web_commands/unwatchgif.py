# coding=utf-8
import main
unwatch = main.load_code_as_module('watchgif').unwatch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    unwatch(bot, chat_id, message)


