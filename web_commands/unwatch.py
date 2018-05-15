# coding=utf-8
import main
unwatch = main.get_platform_command_code('telegram', 'watch').unwatch

def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    unwatch(bot, chat_id, message)


