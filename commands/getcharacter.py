# coding=utf-8
import json
import urllib

import main
retry_on_telegram_error = main.load_code_as_module('retry_on_telegram_error')


def run(bot, chat_id, user, keyConfig, message, total_requested_results=1):
    requestText = str(message).strip()

    url = 'https://eu.api.battle.net/wow/character/jaedenar/' + requestText + '?locale=en_US&apikey=' + keyConfig.get('WOW', 'KEY')
    data = json.load(urllib.urlopen(url))
    if 'Error' not in data and 'thumbnail' in data and not data['thumbnail'] == 'N/A':
        requestText = (user + ', ' if not user == '' else '') + str(data['name']) + ' the level ' + str(data['level']) + ' ' + ResolveRaceID(int(data['race'])) + ' ' + ResolveClassID(int(data['class']))
        imagelink = 'http://render-eu.worldofwarcraft.com/character/' + data['thumbnail'] + '?apikey=' + keyConfig.get('WOW', 'KEY')
        retry_on_telegram_error.SendPhotoWithRetry(bot, chat_id, imagelink, requestText)
        return requestText + '\n' + imagelink
    else:
        return 'I\'m sorry ' + (
        user if not user == '' else 'Dave') + ', I\'m afraid I can\'t find any characters named ' + \
               requestText.encode('utf-8') + '.'

def ResolveClassID(id):
    if id == 1:
        return 'Warrior'
    elif id == 2:
        return 'Paladin'
    elif id == 3:
        return 'Hunter'
    elif id == 4:
        return 'Rogue'
    elif id == 5:
        return 'Priest'
    elif id == 6:
        return 'Death Knight'
    elif id == 7:
        return 'Shaman'
    elif id == 8:
        return 'Mage'
    elif id == 9:
        return 'Warlock'
    elif id == 10:
        return 'Monk'
    elif id == 11:
        return 'Druid'
    elif id == 12:
        return 'Demon Hunter'
    else:
        raise Exception('Unrecognized class id: ' + id + '.')

def ResolveRaceID(id):
    if id == 1:
        return 'Human'
    elif id == 2:
        return 'Orc'
    elif id == 3:
        return 'Dwarf'
    elif id == 4:
        return 'Night Elf'
    elif id == 5:
        return 'Undead'
    elif id == 6:
        return 'Tauren'
    elif id == 7:
        return 'Gnome'
    elif id == 8:
        return 'Troll'
    elif id == 9:
        return 'Blood Elf'
    elif id == 10:
        return 'Draenei'
    elif id == 11:
        return 'Pandarian'
    elif id == 12:
        return 'Nig Nog'
    elif id == 13:
        return 'Nig Nog'
    elif id == 14:
        return 'Nig Nog'
    elif id == 15:
        return 'Nig Nog'
    elif id == 16:
        return 'Nig Nog'
    elif id == 17:
        return 'Nig Nog'
    elif id == 18:
        return 'Nig Nog'
    elif id == 19:
        return 'Nig Nog'
    elif id == 20:
        return 'Nig Nog'
    elif id == 21:
        return 'Nig Nog'
    elif id == 22:
        return 'Nig Nog'
    elif id == 23:
        return 'Nig Nog'
    elif id == 24:
        return 'Nig Nog'
    elif id == 25:
        return 'Nig Nog'
    else:
        raise Exception('Unrecognized race id: ' + str(id) + '.')