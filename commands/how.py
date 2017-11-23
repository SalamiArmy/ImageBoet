# coding=utf-8

from google.appengine.ext import ndb

import main
get = main.load_code_as_module('get')

CommandName = 'how'

class SeenWikiHowLink(ndb.Model):
    # key name: get:str(chat_id)
    allPreviousSeenWikiHowLink = ndb.StringProperty(indexed=False, default='')


# ================================

def setPreviouslySeenWikiHowLinkValue(chat_id, NewValue):
    es = SeenWikiHowLink.get_or_insert(CommandName + ':' + str(chat_id))
    es.allPreviousSeenWikiHowLink = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenWikiHowLinkValue(chat_id, NewValue):
    es = SeenWikiHowLink.get_or_insert(CommandName + ':' + str(chat_id))
    if es.allPreviousSeenWikiHowLink == '':
        es.allPreviousSeenWikiHowLink = NewValue.encode('utf-8')
    else:
        es.allPreviousSeenWikiHowLink += ',' + NewValue.encode('utf-8')
    es.put()

def getPreviouslySeenWikiHowLinkValue(chat_id):
    es = SeenWikiHowLink.get_or_insert(CommandName + ':' + str(chat_id))
    if es:
        return es.allPreviousSeenWikiHowLink.encode('utf-8')
    return ''

def wasPreviouslySeenWikiHowLink(chat_id, how_link):
    allPreviousLinks = getPreviouslySeenWikiHowLinkValue(chat_id)
    if ',' + how_link + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(how_link + ',') or  \
            allPreviousLinks.endswith(',' + how_link) or  \
            allPreviousLinks == how_link:
        return True
    return False


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = message.replace(bot.name, "").strip()
    args, data, results_this_page, total_results = search_gcse_for_how(keyConfig, requestText)
    if totalResults > 1:
        return Send_WikiHowLinks(bot, chat_id, user, requestText, data, total_results, results_this_page, totalResults, args)
    else:
        return Send_First_Valid_WikiHowLink(bot, chat_id, user, requestText, data, total_results, results_this_page)


def search_gcse_for_how(keyConfig, requestText):
    args = {'cx': keyConfig.get('Google', 'GCSE_HOW_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': 'off',
            'q': requestText,
            'start': 1}
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    return args, data, results_this_page, total_results


def Send_First_Valid_WikiHowLink(bot, chat_id, user, requestText, data, total_results, results_this_page):
    if data['searchInformation']['totalResults'] >= '1':
        sent_count = 0
        for item in data['items']:
            how_link = item['link']
            if not wasPreviouslySeenWikiHowLink(chat_id, how_link):
                bot.sendMessage(chat_id=chat_id, text=(user + ', ' if not user == '' else '') + 'how ' + requestText + ': ' + how_link)
                addPreviouslySeenWikiHowLinkValue(chat_id, how_link)
                sent_count += 1
                return [how_link]
    else:
        errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                   ', I don\'t know how ' + requestText
        bot.sendMessage(chat_id=chat_id, text=errorMsg)
        return [errorMsg]


def Send_WikiHowLinks(bot, chat_id, user, requestText, data, total_results, results_this_page, number, args):
    if data['searchInformation']['totalResults'] >= '1':
        total_sent = []
        total_offset = 0
        while len(total_sent) < int(number) and int(total_offset) < int(total_results):
            for item in data['items']:
                xlink = item['link']
                total_offset += 1
                if not wasPreviouslySeenWikiHowLink(chat_id, xlink):
                    bot.sendMessage(chat_id=chat_id, text='how ' + requestText + ' ' + str(len(total_sent)+1)
                                                          + ' of ' + str(number) + ':' + xlink)
                    addPreviouslySeenWikiHowLinkValue(chat_id, xlink)
                    total_sent += 1
                if len(total_sent) >= int(number) or int(total_offset) >= int(total_results):
                    break
            if len(total_sent) < int(number) and int(total_offset) < int(total_results):
                args['start'] = total_offset+1
                data, total_results, results_this_page = get.Google_Custom_Search(args)
        if len(total_sent) < int(number):
            bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                  ', I\'m afraid I cannot find enough ways ' + requestText + '.' +
                                                  ' I could only find ' + str(total_sent) + ' out of ' + str(number))
        return total_sent
    else:
        errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                   ', I don\'t know how ' + requestText
        bot.sendMessage(chat_id=chat_id, text=errorMsg)
        return [errorMsg]
