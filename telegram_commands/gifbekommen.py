import telegram_commands.getgif as getgif
def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    return getgif.run(bot, chat_id, user, keyConfig, message, totalResults)
