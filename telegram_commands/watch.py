# coding=utf-8
import string

import main
retry_on_telegram_error = main.get_platform_command_code('telegram', 'retry_on_telegram_error')
get = main.get_platform_command_code('telegram', 'get')
getgif = main.get_platform_command_code('telegram', 'getgif')

def run(bot, chat_id, user, keyConfig, message, num_to_send=1):
    requestText = str(message).replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_IMAGE_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': requestText,
            'start': 1}
    single_page_watch(args, bot, chat_id, keyConfig, requestText, user, get)


def send_image_with_watch_message(bot, chat_id, imagelink, keyConfig, requestText, total_sent, user, watch_message):
    print 'sending watch message ' + watch_message
    bot.sendMessage(chat_id=chat_id, text=watch_message)
    if imagelink[-len('.gif'):] == '.gif':
        if retry_on_telegram_error.SendDocumentWithRetry(bot, chat_id, imagelink, requestText):
            total_sent += 1
    else:
        if retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText):
            total_sent += 1
    get.send_url_and_tags(bot, chat_id, imagelink, keyConfig, requestText)
    return total_sent


def unwatch(bot, chat_id, message):
    watches = main.getAllWatches()
    if ',' + str(chat_id) + ':get:' + message + ',' in watches or \
            watches.startswith(str(chat_id) + ':get:' + message + ',') or \
            watches.endswith(',' + str(chat_id) + ':get:' + message) or \
                    watches == str(chat_id) + ':get:' + message:
        main.removeFromAllWatches(str(chat_id) + ':get:' + message)
        bot.sendMessage(chat_id=chat_id, text='Watch for /get ' + message + ' has been removed.')
    else:
        bot.sendMessage(chat_id=chat_id, text='Watch for /get ' + message + ' not found.')

def single_page_watch(args, bot, chat_id, keyConfig, requestText, user, watched_command):
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    if 'items' in data and results_this_page >= 0:
        offset_this_page = 0
        total_sent = 0
        while offset_this_page < results_this_page:
            imagelink = data['items'][offset_this_page]['link']
            offset_this_page += 1
            if '?' in imagelink:
                imagelink = imagelink[:imagelink.index('?')]
            if imagelink[-len('.gif'):] == '.gif':
                is_valid = getgif.is_valid_gif(imagelink, chat_id)
            else:
                is_valid = get.is_valid_image(imagelink, chat_id)
            if is_valid:
                if user != 'Watcher':
                    if total_sent == 0 and not main.AllWatchesContains(watched_command.CommandName, chat_id,
                                                                       requestText):
                        watch_message = 'Now watching /' + watched_command.CommandName + ' ' + requestText + '.'
                    else:
                        watch_message = 'Watched /' + watched_command.CommandName + ' ' + requestText + ' changed' + '.'
                    total_sent = send_image_with_watch_message(bot, chat_id, imagelink, keyConfig, requestText,
                                                               total_sent, user, watch_message)
                else:
                    total_sent = send_image_with_watch_message(bot, chat_id, imagelink, keyConfig, requestText,
                                                               total_sent, user,
                                                               'Watched /' + watched_command.CommandName +
                                                               ' ' + requestText + ' changed.')
        if total_sent == 0:
            if user != 'Watcher':
                bot.sendMessage(chat_id=chat_id, text=user + ', watch for /' +
                                                      watched_command.CommandName + ' ' + requestText + ' has not changed.')
        if not main.AllWatchesContains(watched_command.CommandName, chat_id, requestText):
            main.addToAllWatches(watched_command.CommandName, chat_id, requestText)
    else:
        if user != 'Watcher':
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I can\'t find any results for /' +
                                                  watched_command.CommandName + ' ' +
                                                  string.capwords(requestText.encode('utf-8')))