# coding=utf-8
import main
get = main.get_platform_command_code('telegram', 'get')


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.encode('utf-8').replace(bot.name, "").strip()
    return bot.leaveChat(int(requestText))
