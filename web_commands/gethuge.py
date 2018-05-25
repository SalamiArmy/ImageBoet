# coding=utf-8
import main
get = main.get_platform_command_code('telegram', 'get')


def run(keyConfig, message, totalResults=1):
    requestText = message.encode('utf-8').replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_IMAGE_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            "imgSize": "huge"}
    return get.Send_Images(requestText, args, keyConfig, totalResults)


