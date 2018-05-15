import ConfigParser
import unittest

import telegram
from google.appengine.ext import ndb
from google.appengine.ext import testbed

from commands import add


class TestGetHow(unittest.TestCase):
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

    def test_how_multiget(self):
        requestText = 'trippy asian'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_PRIVATE_CHAT_ID')

        add.setTelegram_CommandCode('get', open('../telegram_commands/get.py').read())

        import telegram_commands.how as how
        bot.sendMessage(chat_id=chatId, text=how.run('Admin', requestText, chatId, 2))

    def test_how_group(self):
        requestText = 'nightman'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        keyConfig.read(["bot_keys.ini", "..\\bot_keys.ini"])
        bot = telegram.Bot(keyConfig.get('BotIDs', 'TESTING_TELEGRAM_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_TELEGRAM_GROUP_CHAT_ID')

        add.setTelegram_CommandCode('retry_on_telegram_error', open('../telegram_commands/retry_on_telegram_error.py').read())
        add.setTelegram_CommandCode('get', open('../telegram_commands/get.py').read())

        import telegram_commands.how as how
        bot.sendMessage(chat_id=chatId, text=how.run('Admin', requestText, chatId))
