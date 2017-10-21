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

    def test_watchgif(self):
        requestText = 'sex wagon'

        keyConfig = ConfigParser.ConfigParser()
        keyConfig.read(["keys.ini", "..\keys.ini"])
        bot = telegram.Bot(keyConfig.get('Telegram', 'TELE_BOT_ID'))
        chatId = keyConfig.get('BotAdministration', 'TESTING_PRIVATE_CHAT_ID')

        add.setCommandCode('retry_on_telegram_error', open('../commands/retry_on_telegram_error.py').read())
        add.setCommandCode('get', open('../commands/get.py').read())
        add.setCommandCode('getgif', open('../commands/getgif.py').read())
        add.setCommandCode('watch', open('../commands/watch.py').read())

        import commands.watchgif as watchgif
        watchgif.run(bot, chatId, 'SalamiArmy', keyConfig, requestText)
