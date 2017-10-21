# coding=utf-8
import main
getlarge = main.load_code_as_module('getlarge')
getxlarge = main.load_code_as_module('getxlarge')
getxxlarge = main.load_code_as_module('getxxlarge')
gethuge = main.load_code_as_module('gethuge')


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    getlarge.run(bot, chat_id, user, keyConfig, requestText)
    getxlarge.run(bot, chat_id, user, keyConfig, requestText)
    getxxlarge.run(bot, chat_id, user, keyConfig, requestText)
    gethuge.run(bot, chat_id, user, keyConfig, requestText)
