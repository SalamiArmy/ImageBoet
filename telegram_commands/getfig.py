# coding=utf-8
import main
get = main.get_platform_command_code('telegram', 'get')


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = "a fig"
    args = {'cx': keyConfig.get('Google', 'GCSE_IMAGE_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': 'fig',
            'start': 1}
    return get.Send_Images(bot, chat_id, user, requestText, args, keyConfig, totalResults)
