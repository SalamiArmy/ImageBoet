# coding=utf-8
import main
unwatch = main.get_platform_command_code('telegram', 'watchgifs').unwatch

def run(bot, chat_id, user='Dave', keyConfig=None, message='', totalResults=1):
    unwatch(bot, chat_id)


