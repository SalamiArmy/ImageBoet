import main
getgif = main.get_platform_command_code('telegram', 'getgif')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    getgif.run(bot, chat_id, user, keyConfig, message, totalResults)
