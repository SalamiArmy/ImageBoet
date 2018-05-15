# coding=utf-8
import hashlib
import sys

import logging

reload(sys)
sys.setdefaultencoding('utf8')
import json
import string
import urllib

import io

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import main
retry_on_telegram_error = main.get_platform_command_code('telegram', 'retry_on_telegram_error')
telegram_get = main.get_platform_command_code('telegram', 'get')

CommandName = 'get'

class SeenImageUrls(ndb.Model):
    # key name: ImageUrl
    seenImage = ndb.BooleanProperty(indexed=False, default=False)

class SeenHashDigests(ndb.Model):
    # key name: ImageHash
    seenHash = ndb.BooleanProperty(indexed=False, default=False)

# ================================

def addPreviouslySeenImagesValue(image_url):
    es = SeenImageUrls.get_or_insert(image_url)
    es.seenImage = True
    es.put()

def addPreviouslySeenHashDigest(image_hash):
    es = SeenHashDigests.get_or_insert(image_hash)
    es.seenHash = True
    es.put()

def getSeenImagesValue(image_link):
    es = SeenImageUrls.get_or_insert(image_link)
    return es.seenImage

def getSeenHashDigest(image_hash):
    es = SeenHashDigests.get_or_insert(image_hash)
    return es.seenHash


def wasPreviouslySeenImage(image_link):
    seenImage = getSeenImagesValue(image_link)
    if seenImage:
        return True
    addPreviouslySeenImagesValue(image_link)
    return False

def wasPreviouslySeenHash(image_hash):
    allWhoveSeenHash = getSeenHashDigest(image_hash)
    if allWhoveSeenHash:
        return True
    addPreviouslySeenHashDigest(image_hash)
    return False


def run(keyConfig, message, totalResults=1):
    args = {'cx': keyConfig.get('Google', 'GCSE_IMAGE_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': message,
            'start': 1}
    return Send_Images(message, args, keyConfig, totalResults)


def Google_Custom_Search(args):
    googurl = 'https://www.googleapis.com/customsearch/v1'
    realUrl = googurl + '?' + urllib.urlencode(args)
    data = json.loads(urlfetch.fetch(realUrl).content)
    total_results = 0
    results_this_page = 0
    if 'searchInformation' in data and 'totalResults' in data['searchInformation']:
        total_results = data['searchInformation']['totalResults']
    if 'queries' in data and 'request' in data['queries'] and len(data['queries']['request']) > 0 and 'count' in \
            data['queries']['request'][0]:
        results_this_page = data['queries']['request'][0]['count']
    return data, total_results, results_this_page

def is_valid_image(image_url):
    if image_url != '' and \
            not image_url.startswith('x-raw-image:///') and \
            not wasPreviouslySeenImage(image_url):
        return IsValidImageFile(image_url)
    return False

def ImageHasUniqueHashDigest(image_as_string):
    image_as_hash = hashlib.md5(image_as_string)
    image_hash_digest = image_as_hash.hexdigest()
    logging.info('hashed image as ' + image_hash_digest)
    hashed_before = wasPreviouslySeenHash(image_hash_digest)
    if hashed_before:
        logging.info('Hash collision!')
    return not hashed_before

def IsValidImageFile(image_url):
    global image_file, fd
    try:
        fd = urllib.urlopen(image_url)
        image_file = io.BytesIO(fd.read())
    except IOError:
        return False
    else:
        return telegram_get.ImageIsSmallEnough(image_file) and ImageHasUniqueHashDigest(image_file.getvalue())
    finally:
        try:
            if image_file:
                image_file.close()
            if fd:
                fd.close()
        except UnboundLocalError:
            print("image_file or fd local not defined")
        except NameError:
            print("image_file or fd global not defined")


def Send_Images(requestText, args, keyConfig, total_number_to_send=1):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset, total_results, total_sent = search_results_walker(args, data, total_number_to_send, requestText, results_this_page,
                                                                        total_results, keyConfig)
        if len(total_sent) < int(total_number_to_send):
            if int(total_number_to_send) > 1:
                total_sent.append('I\'m sorry Dave, I\'m afraid I can\'t find any more images for ' + \
                                                      requestText + '. I could only find ' + str(
                                                          len(total_sent)) + ' out of ' + str(total_number_to_send)))
            else:
                total_sent.append('I\'m sorry Dave, I\'m afraid I can\'t find any images for ' + requestText)
        return total_sent
    else:
        if 'error' in data:
            errorMsg = 'I\'m sorry Dave' + data['error']['message']
            return [errorMsg]
        else:
            errorMsg = 'I\'m sorry Dave, I\'m afraid I can\'t find any images for ' + requestText
            return [errorMsg]

def search_results_walker(args, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_offset=0, total_sent=[]):
    offset_this_page = 0
    while len(total_sent) < int(number) and int(offset_this_page) < int(results_this_page):
        imagelink = str(data['items'][offset_this_page]['link'])
        offset_this_page += 1
        total_offset = int(total_offset) + 1
        if '?' in imagelink:
            imagelink = imagelink[:imagelink.index('?')]
        if is_valid_image(imagelink):
            if number == 1:
                total_sent.append(get_url_and_tags(imagelink, keyConfig, requestText))
            else:
                total_sent.append(requestText + ': ' +
                          (str(len(total_sent) + 1) + ' of ' +
                           str(number) + '\n' if int(number) > 1 else '') + imagelink)
    if len(total_sent) < int(number) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = Google_Custom_Search(args)
        return search_results_walker(args, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_offset, total_sent)
    return total_offset, total_results, total_sent

def get_url_and_tags( imagelink, keyConfig, requestText):
    imagelink_str = str(imagelink)
    image_tags = telegram_get.Image_Tags(imagelink_str, keyConfig)
    return requestText + (' ' + image_tags if image_tags != '' else '') + '\n' + imagelink_str
