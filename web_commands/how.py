# coding=utf-8
import ConfigParser

from google.appengine.ext import ndb

import main
get = main.get_platform_command_code('telegram', 'get')

CommandName = 'how'

class SeenWikiHowLink(ndb.Model):
    allPreviousSeenWikiHowLink = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setPreviouslySeenWikiHowLinkValue(NewValue):
    es = SeenWikiHowLink.get_or_insert(CommandName)
    es.allPreviousSeenWikiHowLink = NewValue.encode('utf-8')
    es.put()

def addPreviouslySeenWikiHowLinkValue(NewValue):
    es = SeenWikiHowLink.get_or_insert(CommandName)
    if es.allPreviousSeenWikiHowLink == '':
        es.allPreviousSeenWikiHowLink = NewValue.encode('utf-8')
    else:
        es.allPreviousSeenWikiHowLink += ',' + NewValue.encode('utf-8')
    es.put()

def getPreviouslySeenWikiHowLinkValue():
    es = SeenWikiHowLink.get_or_insert(CommandName)
    if es:
        return es.allPreviousSeenWikiHowLink.encode('utf-8')
    return ''

def wasPreviouslySeenWikiHowLink(how_link):
    allPreviousLinks = getPreviouslySeenWikiHowLinkValue()
    if ',' + how_link + ',' in allPreviousLinks or \
            allPreviousLinks.startswith(how_link + ',') or  \
            allPreviousLinks.endswith(',' + how_link) or  \
            allPreviousLinks == how_link:
        return True
    return False


def run(keyConfig, message, totalResults=1):
    requestText = str(message).strip()
    keyConfig = ConfigParser.ConfigParser()
    keyConfig.read(["keys.ini", "..\keys.ini"])

    args, data, results_this_page, total_results = search_gcse_for_how(keyConfig, requestText)
    if totalResults > 1:
        return Send_WikiHowLinks(requestText, data, total_results, results_this_page, totalResults, args)
    else:
        return Send_First_Valid_WikiHowLink(requestText, data, total_results, results_this_page)


def search_gcse_for_how(keyConfig, requestText):
    args = {'cx': keyConfig.get('Google', 'GCSE_HOW_SE_ID'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'safe': 'off',
            'q': requestText,
            'start': 1}
    data, total_results, results_this_page = get.Google_Custom_Search(args)
    return args, data, results_this_page, total_results


def Send_First_Valid_WikiHowLink(requestText, data, total_results, results_this_page):
    if data['searchInformation']['totalResults'] >= '1':
        sent_count = 0
        for item in data['items']:
            how_link = item['link']
            if not wasPreviouslySeenWikiHowLink(how_link):
                addPreviouslySeenWikiHowLinkValue(how_link)
                if is_valid_how_link(how_link):
                    how_text = 'how ' + requestText + ': ' + how_link
                    sent_count += 1
                    return how_text
    else:
        return 'I\'m sorry Dave, I don\'t know how ' + requestText


def is_valid_how_link(how_link):
    return 'www.wikihow.com/User:' not in how_link


def Send_WikiHowLinks(requestText, data, total_results, results_this_page, number, args):
    if data['searchInformation']['totalResults'] >= '1':
        total_sent = ''
        total_offset = 0
        while len(total_sent.split('\n')) < int(number) and int(total_offset) < int(total_results):
            for item in data['items']:
                xlink = item['link']
                total_offset += 1
                if is_valid_how_link(xlink) and not wasPreviouslySeenWikiHowLink(xlink):
                    addPreviouslySeenWikiHowLinkValue(xlink)
                    total_sent += ('\n' if total_sent != '' else '') + 'how ' + requestText + ' ' + str(len(total_sent.split('\n'))+1)\
                                                          + ' of ' + str(number) + ':' + xlink
                if len(total_sent.split('\n')) >= int(number) or int(total_offset) >= int(total_results):
                    break
            if len(total_sent.split('\n')) < int(number) and int(total_offset) < int(total_results):
                args['start'] = total_offset+1
                data, total_results, results_this_page = get.Google_Custom_Search(args)
        if len(total_sent.split('\n')) < int(number):
            total_sent += ('\n' if total_sent == '' else '') + 'I\'m sorry Dave, I\'m afraid I cannot find enough ways ' + requestText + '.' +\
                          ' I could only find ' + str(len(total_sent.split('\n'))) + ' out of ' + str(number)
        return total_sent
    else:
        return 'I\'m sorry Dave, I don\'t know how ' + requestText
