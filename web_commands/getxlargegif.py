# coding=utf-8
import main
getgif = main.get_platform_command_code('telegram', 'getgif')


def run(keyConfig, message, totalResults=1):
    requestText = message.strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_GIF_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': "image",
            'safe': "off",
            'q': requestText,
            'fileType': 'gif',
            'start': 1,
            'imgSize': 'xlarge'}
    return getgif.Send_Animated_Gifs(requestText, args, keyConfig, totalResults)
