# coding=utf-8

from google.appengine.ext import ndb

import main
get = main.get_platform_command_code('telegram', 'get')

CommandName = 'getxxx'

class SeenXXX(ndb.Model):
    # key name: get:str(chat_id)
    allPreviousSeenXXX = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenXXXValue(chat_id, NewValue):
    es = SeenXXX.get_or_insert(CommandName + ':' + str(chat_id))
    es.allPreviousSeenXXX = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenXXXValue(chat_id, NewValue):
    es = SeenXXX.get_or_insert(CommandName + ':' + str(chat_id))
    if es.allPreviousSeenXXX == '':
        es.allPreviousSeenXXX = NewValue.encode('utf-8')
    else:
        es.allPreviousSeenXXX += ',' + NewValue.encode('utf-8')
    es.put()

def getPreviouslySeenXXXValue(chat_id):
    es = SeenXXX.get_or_insert(CommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenXXX.encode('utf-8')
    return ''

def wasPreviouslySeenXXX(chat_id, xxx_link):
    allPreviousLinks = getPreviouslySeenXXXValue(chat_id)
    if ',' + xxx_link + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(xxx_link + ',') or  \
            allPreviousLinks.endswith(',' + xxx_link) or  \
            allPreviousLinks == xxx_link:
        return True
    return False


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    args, data, results_this_page, total_results = search_gcse_for_xxx(keyConfig, requestText)
    if 'error' in data:
        errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                   ', ' + data['error']['message']
        bot.sendMessage(chat_id=chat_id, text=errorMsg)
        return [errorMsg]
    if totalResults > 1:
        return Send_XXXs(bot, chat_id, user, requestText, data, total_results, results_this_page, totalResults, args)
    else:
        return Send_First_Valid_XXX(bot, chat_id, user, requestText, data, total_results, results_this_page)


def search_gcse_for_xxx(keyConfig, requestText):
    args = {'cx': keyConfig.get('Google', 'GCSE_XSE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': 'off',
            'q': requestText,
            'start': 1}
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    return args, data, results_this_page, total_results


def Send_First_Valid_XXX(bot, chat_id, user, requestText, data, total_results, results_this_page):
    if data['searchInformation']['totalResults'] >= '1':
        sent_count = 0
        for item in data['items']:
            xlink = item['link']
            if is_valid_xxx(xlink) and not wasPreviouslySeenXXX(chat_id, xlink):
                bot.sendMessage(chat_id=chat_id, text=(user + ', ' if not user == '' else '') + requestText + ': ' + xlink)
                addPreviouslySeenXXXValue(chat_id, xlink)
                sent_count += 1
                return [xlink]
    errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
               ', you\'re just too filthy.'
    bot.sendMessage(chat_id=chat_id, text=errorMsg)
    return [errorMsg]


def is_valid_xxx(xlink):
    return not xlink.endswith('/replies') and \
           'search?search=' not in xlink and \
           not ('heavy-r.com' in xlink and xlink.endswith('.html'))


def Send_XXXs(bot, chat_id, user, requestText, data, total_results, results_this_page, number, args):
    if data['searchInformation']['totalResults'] >= '1':
        total_sent = []
        total_offset = 0
        while len(total_sent) < int(number) and int(total_offset) < int(total_results):
            for item in data['items']:
                xlink = item['link']
                total_offset += 1
                if is_valid_xxx(xlink) and not wasPreviouslySeenXXX(chat_id, xlink):
                    bot.sendMessage(chat_id=chat_id, text=requestText + ' ' + str(len(total_sent)+1)
                                                          + ' of ' + str(number) + ':' + xlink)
                    addPreviouslySeenXXXValue(chat_id, xlink)
                    total_sent += xlink
                if len(total_sent) >= int(number) or int(total_offset) >= int(total_results):
                    break
            if len(total_sent) < int(number) and int(total_offset) < int(total_results):
                args['start'] = total_offset+1
                data, total_results, results_this_page = get.Google_Custom_Search(args)
        if len(total_sent) < int(number):
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I cannot find enough filth for ' + requestText + '.' +
                                                  ' I could only find ' + len(total_sent) + ' out of ' + str(number))
        return total_sent
    else:
        errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                   ', you\'re just too filthy.'
        bot.sendMessage(chat_id=chat_id, text=errorMsg)
        return [errorMsg]
