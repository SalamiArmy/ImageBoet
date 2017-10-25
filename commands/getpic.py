# coding=utf-8
import main
getlarge = main.load_code_as_module('getlarge')
getxlarge = main.load_code_as_module('getxlarge')
getxxlarge = main.load_code_as_module('getxxlarge')
gethuge = main.load_code_as_module('gethuge')


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getlarge ' + requestText + ':')
    getlarge.run(bot, chat_id, user, keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getxlarge ' + requestText + ':')
    getxlarge.run(bot, chat_id, user, keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getxxlarge ' + requestText + ':')
    getxxlarge.run(bot, chat_id, user, keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /gethuge ' + requestText + ':')
    gethuge.run(bot, chat_id, user, keyConfig, requestText)
