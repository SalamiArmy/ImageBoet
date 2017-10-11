# coding=utf-8
import ConfigParser
import unittest

import telegram
from commands import add

from google.appengine.ext import ndb
from google.appengine.ext import testbed


class TestGet(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_user_stub()
        self.testbed.init_urlfetch_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_getgif(self):
        requestText = 'tonguing asshole'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(['bot_keys.ini', '..\\bot_keys.ini'])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        _code_file = open('../commands/retry_on_telegram_error.py').read()
        add.setCommandCode('retry_on_telegram_error', _code_file)
        add.setCommandCode('get', open('../commands/get.py').read())

        keyConfig.read(['keys.ini', '..\\keys.ini'])

        import commands.getgif as getgif
        getgif.run(bot, chatId, 'Admin', keyConfig, requestText, 10)
