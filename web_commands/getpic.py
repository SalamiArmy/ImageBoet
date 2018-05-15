# coding=utf-8
import main
getlarge = main.get_platform_command_code('telegram', 'getlarge')
getxlarge = main.get_platform_command_code('telegram', 'getxlarge')
getxxlarge = main.get_platform_command_code('telegram', 'getxxlarge')
gethuge = main.get_platform_command_code('telegram', 'gethuge')


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    returnMsg = []
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getlarge ' + requestText + ':')
    returnMsg += getlarge.run(bot, chat_id, user, keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getxlarge ' + requestText + ':')
    returnMsg += getxlarge.run(bot, chat_id, user, keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getxxlarge ' + requestText + ':')
    returnMsg += getxxlarge.run(bot, chat_id, user, keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /gethuge ' + requestText + ':')
    returnMsg += gethuge.run(bot, chat_id, user, keyConfig, requestText)
    return returnMsg
