# coding=utf-8
import main
getlarge = main.get_platform_command_code('telegram', 'getlarge')
getxlarge = main.get_platform_command_code('telegram', 'getxlarge')
getxxlarge = main.get_platform_command_code('telegram', 'getxxlarge')
gethuge = main.get_platform_command_code('telegram', 'gethuge')


def run(keyConfig, message, totalResults=1):
    requestText = message.strip()
    returnMsg = []
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getlarge ' + requestText + ':')
    returnMsg += getlarge.run(keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getxlarge ' + requestText + ':')
    returnMsg += getxlarge.run(keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /getxxlarge ' + requestText + ':')
    returnMsg += getxxlarge.run(keyConfig, requestText)
    bot.sendMessage(chat_id=chat_id, text=(user if not user == '' else 'Dave') +
                                          ', /gethuge ' + requestText + ':')
    returnMsg += gethuge.run(keyConfig, requestText)
    return returnMsg
