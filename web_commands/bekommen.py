import main
get = main.get_platform_command_code('telegram', 'get')
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    return get.run(bot, chat_id, user, keyConfig, message, totalResults)
