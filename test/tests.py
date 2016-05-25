import os
import server
import unittest
from database.sampledata import Sampledata

sd = Sampledata()


class TestCase(unittest.TestCase):
    testMode = False #flag is switched to signal test mode if called from main


    def setUp(self):
        self.app = server.app.test_client()
        self.testJSONs = sd.getTestJSONs()
        print 'setup app'


    def tearDown(self):
        pass

    def test_empty_db(self):
        self.app.post('/fbchatbot/', data=self.testJSONs[0], follow_redirects=True)
        # self.app.post('/fbchatbot/', data=self.testJSONs[1], follow_redirects=True)
        print 'getting facebookchatbot..'


if __name__ == '__main__':
    unittest.main()
