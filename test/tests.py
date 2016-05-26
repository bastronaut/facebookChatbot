import os
import server
import unittest
from database.sampledata import Sampledata

sd = Sampledata()


class TestCase(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()
        self.testJSONs = sd.getTestJSONs()
        print 'setup app'

    def tearDown(self):
        pass

    def test_verifytoken(self):
        self.app.get('/fbchatbot/')

    def test_incomingPOST(self):
        self.app.post('/fbchatbot/',
                      data=self.testJSONs[0], follow_redirects=True)
        print 'getting facebookchatbot..'


if __name__ == '__main__':
    unittest.main()
