# coding=utf-8

from google.appengine.ext import ndb

import main
get = main.get_platform_command_code('telegram', 'get')

CommandName = 'getxxx'

class SeenXXX(ndb.Model):
    allPreviousSeenXXX = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setPreviouslySeenXXXValue(NewValue):
    es = SeenXXX.get_or_insert(CommandName)
    es.allPreviousSeenXXX = NewValue
    es.put()

def addPreviouslySeenXXXValue(NewValue):
    es = SeenXXX.get_or_insert(CommandName)
    if es.allPreviousSeenXXX == '':
        es.allPreviousSeenXXX = NewValue
    else:
        es.allPreviousSeenXXX += ',' + NewValue
    es.put()

def getPreviouslySeenXXXValue():
    es = SeenXXX.get_or_insert(CommandName)
    if es:
        return es.allPreviousSeenXXX
    return ''

def wasPreviouslySeenXXX(xxx_link):
    allPreviousLinks = getPreviouslySeenXXXValue()
    if ',' + xxx_link + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(xxx_link + ',') or  \
            allPreviousLinks.endswith(',' + xxx_link) or  \
            allPreviousLinks == xxx_link:
        return True
    return False


def run(keyConfig, message, totalResults=1):
    requestText = message.strip()
    args, data, results_this_page, total_results = search_gcse_for_xxx(keyConfig, requestText)
    if totalResults > 1:
        return Send_XXXs(requestText, data, total_results, results_this_page, totalResults, args)
    else:
        return Send_First_Valid_XXX(requestText, data, total_results, results_this_page)


def search_gcse_for_xxx(keyConfig, requestText):
    args = {'cx': keyConfig.get('Google', 'GCSE_XSE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': 'off',
            'q': requestText,
            'start': 1}
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    return args, data, results_this_page, total_results


def Send_First_Valid_XXX(requestText, data, total_results, results_this_page):
    if data['searchInformation']['totalResults'] >= '1':
        sent_count = 0
        for item in data['items']:
            xlink = item['link']
            if is_valid_xxx(xlink) and not wasPreviouslySeenXXX(xlink):
                addPreviouslySeenXXXValue(xlink)
                sent_count += 1
                return [xlink]
    errorMsg = 'I\'m sorry Dave, you\'re just too filthy.'
    return [errorMsg]


def is_valid_xxx(xlink):
    return 'xvideos.com/tags/' not in xlink and \
           'xvideos.com/favorite/' not in xlink and \
           'xvideos.com/?k=' not in xlink and \
           'xvideos.com/tags' not in xlink and \
           'xvideos.com/profiles/' not in xlink and \
           'pornhub.com/users/' not in xlink and \
           'pornhub.com/video/search?search=' not in xlink and \
           'pornhub.com/insights/' not in xlink and \
           'pornhub.com/devices/' not in xlink and \
           'pornhub.com/gay/' not in xlink and \
           'pornhub.com/pornstar/' not in xlink and \
           'xnxx.com/?' not in xlink and \
           'xnxx.com/search/' not in xlink and \
           'xnxx.com/tags/' not in xlink and \
           'xhamster.com/categories/' not in xlink and \
           'xhamster.com/channels/' not in xlink and \
           'xhamster.com/forums/' not in xlink and \
           'xhamster.com/stories_search' not in xlink and \
           'xhamster.com/stories/' not in xlink and \
           'xhamster.com/search/stories?q=' not in xlink and \
           'xhamster.com/user/' not in xlink and \
           'xhamster.com/search?q=' not in xlink and \
           'redtube.com/pornstar/' not in xlink and \
           'redtube.com/?search=' not in xlink and \
           'motherless.com/term/' not in xlink and \
           'search?search=' not in xlink


def Send_XXXs(requestText, data, total_results, results_this_page, number, args):
    if data['searchInformation']['totalResults'] >= '1':
        total_sent = []
        total_offset = 0
        while len(total_sent) < int(number) and int(total_offset) < int(total_results):
            for item in data['items']:
                xlink = item['link']
                total_offset += 1
                if is_valid_xxx(xlink) and not wasPreviouslySeenXXX(xlink):
                    addPreviouslySeenXXXValue(xlink)
                    total_sent += xlink
                if len(total_sent) >= int(number) or int(total_offset) >= int(total_results):
                    break
            if len(total_sent) < int(number) and int(total_offset) < int(total_results):
                args['start'] = total_offset+1
                data, total_results, results_this_page = get.Google_Custom_Search(args)
        if len(total_sent) < int(number):
            total_sent += 'I\'m sorry Dave, I\'m afraid I cannot find enough filth for ' + requestText + '.' + \
                                                  ' I could only find ' + len(total_sent) + ' out of ' + str(number)
        return total_sent
    else:
        errorMsg = 'I\'m sorry Dave, you\'re just too filthy.'
        return [errorMsg]
