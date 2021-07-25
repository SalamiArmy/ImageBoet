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
    return 'xvideos.com/tags/' not in xlink and \
           'xvideos.com/favorite/' not in xlink and \
           'xvideos.com/?k=' not in xlink and \
           'xvideos.com/tags' not in xlink and \
           'xvideos.com/profiles/' not in xlink and \
           'xvideos.com/pornstars/' not in xlink and \
           'xvideos.com/channels/' not in xlink and \
           'xvideos.com/model-channels/' not in xlink and \
           'xvideos.com/c/month/' not in xlink and \
           'pornhub.com/users/' not in xlink and \
           'pornhub.com/video/search?search=' not in xlink and \
           'pornhub.com/insights/' not in xlink and \
           'pornhub.com/devices/' not in xlink and \
           'pornhub.com/gay/' not in xlink and \
           'pornhub.com/press/' not in xlink and \
           'pornhub.com/pornstar/' not in xlink and \
           'pornhub.com/popularwithwomen' not in xlink and \
           'pornhub.com/partners/' not in xlink and \
           'pornhub.com/playlist/' not in xlink and \
           'pornhub.com/model/' not in xlink and \
           'pornhub.com/blog/' not in xlink and \
           'pornhub.com/channels/' not in xlink and \
           'pornhub.com/tags/' not in xlink and \
           'pornhub.com/jobs/' not in xlink and \
           'porntube.com/search?' not in xlink and \
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
           'xhamster.com/search/photos?q=' not in xlink and \
           'xhamster.com/photos/categories/' not in xlink and \
           'xhamster.com/blog/' not in xlink and \
           'xhamster.com/search/photos' not in xlink and \
           'xhamster.com/photos/gallery/' not in xlink and \
           'xhamster.com/tags/' not in xlink and \
           'xhamster.com/search?' not in xlink and \
           'xhamster.com/gay/' not in xlink and \
           'xhamster.com/info/' not in xlink and \
           'xhamster.com/celebrities/' not in xlink and \
           'redtube.com/pornstar/' not in xlink and \
           'redtube.com/?search=' not in xlink and \
           'redtube.com/gay?search=' not in xlink and \
           'redtube.com/channels/' not in xlink and \
           'motherless.com/term/' not in xlink and \
           'motherless.com/groups/member/' not in xlink and \
           not xlink.endswith('/replies') and \
           'search?search=' not in xlink and \
           'youporn.com/porntags/' not in xlink and \
           'youporn.com/category/' not in xlink and \
           'youporn.com/channel/' not in xlink and \
           'youporn.com/search/?query=' not in xlink and \
           'youporn.com/contentpartnerprogram' not in xlink and \
           'youporn.com/pornstar/' not in xlink and \
           'youporn.com/country/' not in xlink and \
           'eporner.com/gifs/' not in xlink and \
           'eporner.com/photo/' not in xlink and \
           'eporner.com/search/' not in xlink and \
           'eporner.com/search-photos/' not in xlink and \
           'eporner.com/buscar-fotos/roll/' not in xlink and \
           'eporner.com/pornstar/' not in xlink and \
           'orgasm.com/free-porn-blog/' not in xlink and \
           'porntrex.com/tags/' not in xlink and \
           'porntrex.com/community/threads/' not in xlink and \
           'porn.com/pics/search?' not in xlink and \
           'porn.com/pornstars/search?' not in xlink and \
           'porn.com/gay/' not in xlink and \
           'porn.com/blog/' not in xlink and \
           'porntrex.com/search/' not in xlink and \
           'beeg.com/tag/' not in xlink and \
           'se.porn.com/videos/search?q=' not in xlink and \
           'spankbang.com/s/' not in xlink and \
           'xnxx.com/pornstar/' not in xlink and \
           'xvideos.com/models/' not in xlink and \
           'xvideos.com/amateur-channels/' not in xlink and \
           'tube8.com/cat/' not in xlink and \
           'tube8.com/searches.html?q=' not in xlink and \
           'xhamster.com/pornstars/' not in xlink and \
           'xhamster.com/photos/search/' not in xlink and \
           'xhamster.com/search/' not in xlink and \
           not ('heavy-r.com' in xlink and xlink.endswith('.html')) and \
           'pornhub.com/pornstars?' not in xlink and \
           'pornhub.com/blog' not in xlink and \
           'xhamster.com/creator-signup' not in xlink and \
           'pornhub.com/content_partner_guide' not in xlink and \
           'pornhub.com/sex/' not in xlink and \
           'xvideos.com/c/' not in xlink and \
           'heavy-r.com/shocking_videos/recent/' not in xlink and \
           'pornhub.com/video?c=' not in xlink and \
           'spankbang.com/pornstar/' not in xlink and \
           'tnaflix.com/search.php?what=' not in xlink and \
           'xvideos.com/pornstar-channels/' not in xlink and \
           'anysex.com/search/?q=' not in xlink


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
