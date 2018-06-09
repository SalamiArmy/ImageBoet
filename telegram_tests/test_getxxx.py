import ConfigParser
import unittest

import telegram
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from commands import add


class TestGetXXX(unittest.TestCase):
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
        # Clear ndb's in-context cache between telegram_tests.
        # This prevents data from leaking between telegram_tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def test_getxxx_multiget(self):
        requestText = 'nonk tits'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        add.setTelegram_CommandCode('get', open('../telegram_commands/get.py').read())

        import telegram_commands.getxxx as getxxx
        getxxx.run(bot, chatId, 'Admin', keyConfig, requestText, 2)

    def test_getxxx_group(self):
        requestText = 'rory gilmore'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TESTING_TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID')

        add.setTelegram_CommandCode('retry_on_telegram_error', open('../telegram_commands/retry_on_telegram_error.py').read())
        add.setTelegram_CommandCode('get', open('../telegram_commands/get.py').read())

        import telegram_commands.getxxx as getxxx
        if getxxx.run(bot, chatId, 'Admin', keyConfig, requestText) is None:
            raise Exception
