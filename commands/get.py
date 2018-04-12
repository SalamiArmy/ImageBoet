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
retry_on_telegram_error = main.load_code_as_module('retry_on_telegram_error')

CommandName = 'get'

class WhosSeenImageUrls(ndb.Model):
    # key name: ImageUrl
    whoseSeenImage = ndb.StringProperty(indexed=False, default='')

class WhosSeenHashDigests(ndb.Model):
    # key name: ImageHash
    whoseSeenHash = ndb.StringProperty(indexed=False, default='')

# ================================

def addPreviouslySeenImagesValue(image_url, chat_id):
    es = WhosSeenImageUrls.get_or_insert(image_url)
    if es.whoseSeenImage == '':
        es.whoseSeenImage = str(chat_id)
    else:
        es.whoseSeenImage += ',' + str(chat_id)
    es.put()

def addPreviouslySeenHashDigest(image_hash, chat_id):
    es = WhosSeenHashDigests.get_or_insert(image_hash)
    if es.whoseSeenHash == '':
        es.whoseSeenHash = str(chat_id)
    else:
        es.whoseSeenHash += ',' + str(chat_id)
    es.put()

def getWhoseSeenImagesValue(image_link):
    es = WhosSeenImageUrls.get_or_insert(image_link)
    if es:
        return str(es.whoseSeenImage)
    return ''

def getWhoseSeenHashDigest(image_hash):
    es = WhosSeenHashDigests.get_or_insert(image_hash)
    if es:
        return str(es.whoseSeenHash)
    return ''


def wasPreviouslySeenImage(image_link, chat_id):
    allWhoveSeenImage = getWhoseSeenImagesValue(image_link)
    if ',' + str(chat_id) + ',' in allWhoveSeenImage or \
            allWhoveSeenImage.startswith(str(chat_id) + ',') or \
            allWhoveSeenImage.endswith(',' + str(chat_id)) or \
                    allWhoveSeenImage == str(chat_id):
        return True
    addPreviouslySeenImagesValue(image_link, chat_id)
    return False

def wasPreviouslySeenHash(image_hash, chat_id):
    allWhoveSeenHash = getWhoseSeenHashDigest(image_hash)
    if ',' + str(chat_id) + ',' in allWhoveSeenHash or \
            allWhoveSeenHash.startswith(str(chat_id) + ',') or \
            allWhoveSeenHash.endswith(',' + str(chat_id)) or \
                    allWhoveSeenHash == str(chat_id):
        return True
    addPreviouslySeenHashDigest(image_hash, chat_id)
    return False


def run(bot, chat_id, user, keyConfig, message, totalResults=1):
    requestText = str(message).replace(bot.name, "").strip()
    args = {'cx': keyConfig.get('Google', 'GCSE_IMAGE_SE_ID1'),
            'key': keyConfig.get('Google', 'GCSE_APP_ID'),
            'searchType': 'image',
            'safe': 'off',
            'q': requestText,
            'start': 1}
    return Send_Images(bot, chat_id, user, requestText, args, keyConfig, totalResults)


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

def is_valid_image(image_url, chat_id):
    if image_url != '' and \
            not image_url.startswith('x-raw-image:///') and \
            not wasPreviouslySeenImage(image_url, chat_id):
        return IsValidImageFile(image_url, chat_id)
    return False

def ImageIsSmallEnough(image_file):
    return int(sys.getsizeof(image_file)) < 10000000

def ImageHasUniqueHashDigest(image_as_string, chat_id):
    image_as_hash = hashlib.md5(image_as_string)
    image_hash_digest = image_as_hash.hexdigest()
    logging.info('hashed image as ' + image_hash_digest)
    hashed_before = wasPreviouslySeenHash(image_hash_digest, chat_id)
    if hashed_before:
        logging.info('Hash collision!')
    return not hashed_before

def IsValidImageFile(image_url, chat_id):
    global image_file, fd
    try:
        fd = urllib.urlopen(image_url)
        image_file = io.BytesIO(fd.read())
    except IOError:
        return False
    else:
        return ImageIsSmallEnough(image_file) and ImageHasUniqueHashDigest(image_file.getvalue(), chat_id)
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

def Image_Tags(imagelink, keyConfig):
    tags = ''
    strPayload = str({
        "requests":
            [
                {
                    "features":
                        [
                            {
                                "type": "WEB_DETECTION"
                            },
                            {
                                "type": "SAFE_SEARCH_DETECTION"
                            }
                        ],
                    "image":
                        {
                            "source":
                                {
                                    "imageUri": str(imagelink)
                                }
                        }
                }
            ]
    })
    try:
        raw_data = urlfetch.fetch(
            url='https://vision.googleapis.com/v1/images:annotate?key=' + keyConfig.get('Google', 'GCSE_APP_ID'),
            payload=strPayload,
            method='POST',
            headers={'Content-type': 'application/json'})
    except:
        return ''
    visionData = json.loads(raw_data.content)
    if 'error' not in visionData:
        if 'error' not in visionData['responses'][0]:
            webDetection = visionData['responses'][0]['webDetection']
            strAdult = visionData['responses'][0]['safeSearchAnnotation']['adult']
            if strAdult == 'POSSIBLE' or \
                strAdult == 'LIKELY' or \
                strAdult == 'VERY_LIKELY':
                tags += 'porn, '
            else:
                strViolence = visionData['responses'][0]['safeSearchAnnotation']['violence']
                if strAdult == 'POSSIBLE' or \
                    strViolence == 'LIKELY' or \
                    strViolence == 'VERY_LIKELY':
                    tags += 'gore, '
                else:
                    strMedical = visionData['responses'][0]['safeSearchAnnotation']['medical']
                    if strAdult == 'POSSIBLE' or \
                        strMedical == 'LIKELY' or \
                        strMedical == 'VERY_LIKELY':
                        tags += 'a medical procedure, '
                    else:
                        strSpoof = visionData['responses'][0]['safeSearchAnnotation']['spoof']
                        if strAdult == 'POSSIBLE' or \
                            strSpoof == 'LIKELY' or \
                            strSpoof == 'VERY_LIKELY':
                            tags += 'a meme, '
            if ('webEntities' in webDetection):
                for entity in webDetection['webEntities']:
                    if 'description' in entity \
                    and str(entity['description']) != 'GIF' \
                    and str(entity['description']) != 'Giphy' \
                    and str(entity['description']) != 'Gfycat' \
                    and str(entity['description']) != 'WebM' \
                    and str(entity['description']) != 'Ogg' \
                    and str(entity['description']) != 'File format' \
                    and str(entity['description']) != 'Internet media type' \
                    and str(entity['description']) != 'MIME' \
                    and str(entity['description']) != 'Image' \
                    and str(entity['description']) != 'Imgur':
                        tags += str(entity['description']) + ', '
        else:
            if visionData['responses'][0]['error']['message'][:10] == 'Image size' and visionData['responses'][0]['error']['message'][19:] == 'exceeding allowed max (4.00M).':
                tags += 'doesn\'t look like anything to me, image is too large ' + visionData['responses'][0]['error']['message'][11:18]
            else:
                print(visionData['responses'][0]['error']['message'])
    else:
        print(visionData['error']['message'])
    if tags != '' and not tags.startswith('doesn\'t look like anything to me'):
        tags = 'looks like: ' + tags
    return tags.rstrip(', ')

def Send_Images(bot, chat_id, user, requestText, args, keyConfig, total_number_to_send=1):
    data, total_results, results_this_page = Google_Custom_Search(args)
    if 'items' in data and total_results > 0:
        total_offset, total_results, total_sent = search_results_walker(args, bot, chat_id, data, total_number_to_send,
                                                                        user + ', ' + requestText, results_this_page,
                                                                        total_results, keyConfig)
        if len(total_sent) < int(total_number_to_send):
            if int(total_number_to_send) > 1:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find any more images for ' +
                                                      string.capwords(requestText.encode('utf-8') + '.' +
                                                                      ' I could only find ' + str(
                                                          len(total_sent)) + ' out of ' + str(total_number_to_send)))
            else:
                bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                      ', I\'m afraid I can\'t find any images for ' +
                                                      string.capwords(requestText.encode('utf-8')))
        return total_sent
    else:
        if 'error' in data:
            errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') +\
                       data['error']['message']
            bot.sendMessage(chat_id=chat_id, text=errorMsg)
            return [errorMsg]
        else:
            errorMsg = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                       ', I\'m afraid I can\'t find any images for ' + \
                       string.capwords(requestText.encode('utf-8'))
            bot.sendMessage(chat_id=chat_id, text=errorMsg)
            return [errorMsg]

def search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                          total_offset=0, total_sent=[]):
    offset_this_page = 0
    while len(total_sent) < int(number) and int(offset_this_page) < int(results_this_page):
        imagelink = str(data['items'][offset_this_page]['link'])
        offset_this_page += 1
        total_offset = int(total_offset) + 1
        if '?' in imagelink:
            imagelink = imagelink[:imagelink.index('?')]
        if is_valid_image(imagelink, chat_id):
            if number == 1:
                if retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText +
                        (' ' + str(len(total_sent) + 1) + ' of ' + str(number) if int(number) > 1 else '')):
                    total_sent.append(imagelink)
                    send_url_and_tags(bot, chat_id, imagelink, keyConfig, requestText)
            else:
                message = requestText + ': ' + \
                          (str(len(total_sent) + 1) + ' of ' + str(number) + '\n' if int(number) > 1 else '') + imagelink
                bot.sendMessage(chat_id, message)
                total_sent.append(imagelink)
    if len(total_sent) < int(number) and int(total_offset) < int(total_results):
        args['start'] = total_offset + 1
        data, total_results, results_this_page = Google_Custom_Search(args)
        return search_results_walker(args, bot, chat_id, data, number, requestText, results_this_page, total_results, keyConfig,
                                     total_offset, total_sent)
    return total_offset, total_results, total_sent

def send_url_and_tags(bot, chat_id, imagelink, keyConfig, requestText):
    imagelink_str = str(imagelink)
    image_tags = Image_Tags(imagelink_str, keyConfig)
    bot.sendMessage(chat_id=chat_id, text=requestText +
                                          (' ' + image_tags if image_tags != '' else '') +
                                          '\n' + imagelink_str,
                    disable_web_page_preview=True)
