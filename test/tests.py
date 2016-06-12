from sets import Set
from database.sampledata import Sampledata
from chatbot.responseBuilderGraph import ResponseBuilderGraph
from chatbot.messageEntity import MessageEntity
import server
import unittest


class TestCase(unittest.TestCase):

    def setUp(self):
        self.sd = Sampledata()
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


class TestResponseBuilderGraph(unittest.TestCase):

    def setUp(self):
        self.sampleconversationtrees = {
            1: {123: set([124, 126]), 124: set([125]), 125: set([]),
                126: set([127, 128]), 127: set([]), 128: set([129]), 129: set([])},
            2: {130: set([131, 132]), 131: set([133, 134]), 132: set([135]),
                133: set([]), 134: set([]), 135: set([])}}
        self.rbg = ResponseBuilderGraph()
        self.rbg.setconversations(self.sampleconversationtrees)
        self.sd = Sampledata()
        self.messages = self.sd.getgraphmessages()

    def test_is_child(self):
        self.assertTrue(self.rbg.is_child(1, 123, 124))
        self.assertTrue(self.rbg.is_child(1, 124, 125))
        self.assertTrue(self.rbg.is_child(2, 132, 135))
        self.assertFalse(self.rbg.is_child(1, 124, 123))
        self.assertFalse(self.rbg.is_child(1, 125, 123))
        self.assertFalse(self.rbg.is_child(2, 999, 123))

    def test_add_node(self):
        self.rbg.add_node(1, 234)
        self.assertTrue(type(self.rbg.conversationtrees[1][234]) == Set)
        self.rbg.add_node(1, 123)
        self.assertTrue(self.rbg.conversationtrees[1][123] ==
                        set([124, 126]))

    def test_remove_node(self):
        remove_result = {123: set([124, 126]), 124: set([125]), 125: set([])}
        self.rbg.remove_node(1, 126)
        self.assertEqual(self.rbg.conversationtrees[1], remove_result)

        remove_result = {123: set([124, 126])}
        self.rbg.remove_node(1, 124)
        self.assertEqual(self.rbg.conversationtrees[1], remove_result)

        self.rbg.remove_node(1, 999)
        self.rbg.remove_node(999, 1)
        self.assertEqual(self.rbg.conversationtrees[1], remove_result)

    def test_remove_edge(self):
        remove_edge_result = {
            123: set([126]), 124: set([125]), 125: set([]),
            126: set([127, 128]), 127: set([]), 128: set([129]), 129: set([])}
        self.rbg.remove_edge(1, 124)
        self.assertEqual(self.rbg.conversationtrees[1], remove_edge_result)

        self.rbg.remove_edge(1, 'DOESNT EXIST')  # result should not change
        self.assertEqual(self.rbg.conversationtrees[1], remove_edge_result)

    def test_add_edge(self):
        add_edge_result = {128: set([129]), 129: set([]), 123: set([124, 125, 126]),
        124: set([125]), 125: set([]), 126: set([128, 127]), 127: set([])}
        self.rbg.add_edge(1, 123, 125)
        self.assertEqual(self.rbg.conversationtrees[1], add_edge_result)

        self.rbg.add_edge(1, 123, 124)  # already exists, result should not change
        self.assertEqual(self.rbg.conversationtrees[1], add_edge_result)

    def test_buildconversationtrees(self):
        convtreesresult = {
            1: {123: set([124, 126]), 124: set([125]), 125: set([]),
                126: set([127, 128]), 127: set([]), 128: set([129]), 129: set([])},
            2: {130: set([131, 132]), 131: set([133, 134]), 132: set([135]),
                133: set([]), 134: set([]), 135: set([])}}
        self.assertEqual(self.rbg.buildconversationtrees(self.messages), convtreesresult)

    def test_getrootnodes(self):
        rootnodes = {1: 123, 2: 130}
        self.assertEqual(self.rbg.getrootnodes(self.messages), rootnodes)

    def test_getchildnodes(self):
        self.assertEqual(self.rbg.getchildnodes(1, 123), set([124, 126]))
        self.assertEqual(self.rbg.getchildnodes(1, 999), None)
        self.assertEqual(self.rbg.getchildnodes(2, 132), set([135]))
        self.assertEqual(self.rbg.getchildnodes(999, 1), None)

    def test_getfollowupnodes(self):
        sampleconvstates = self.sd.getsampleconversationstates()
        self.assertEqual(self.rbg.getfollowupnodes(sampleconvstates['bob']),
                         {1: set([125]), 2: set([133, 134])})
        self.assertEqual(self.rbg.getfollowupnodes(sampleconvstates['hank']),
                         {1: set([]), 2: None})
        self.assertEqual(self.rbg.getfollowupnodes(sampleconvstates['ann']),
                         {999: None})

    def test_getresponseformessages(self):
        messageone = MessageEntity('bob', 'Hi')
        messagetwo = MessageEntity('bob', 'Not great...')
        messagetree = MessageEntity('bob', 'Feeling tired')
        messagefour = MessageEntity('bob', 'I will!')
        messagefive = MessageEntity('bob', 'Good!')
        messagesix = MessageEntity('bob', '')
        messageseven = MessageEntity('bob', 'BLABLABLA999')
        messageeight = MessageEntity('bob', '130')
        messagenine = MessageEntity('bob', '135')
        sampleconvstates = self.sd.getsampleconversationstates()
        self.rbg.setconversationstates(sampleconvstates)
        # first question in a conversation
        self.assertEqual(self.rbg.getresponseformessages(messageone),
                         'Hi! :) How are you?')
        # the followup question
        self.assertEqual(self.rbg.getresponseformessages(messagetwo),
                         'How come?')
        # a repeated message should not receive another reply
        self.assertFalse(self.rbg.getresponseformessages(messagetwo))
        # the followup question after a repeated message should
        self.assertEqual(self.rbg.getresponseformessages(messagetree),
                         'Aww. Get some sleep!')
        # the final message in the chain
        self.assertEqual(self.rbg.getresponseformessages(messagefour),
                         'Good night!')
        # the second question repeated
        self.assertFalse(self.rbg.getresponseformessages(messagefive))
        # testing messages that do not occur
        self.assertFalse(self.rbg.getresponseformessages(messagesix))
        self.assertFalse(self.rbg.getresponseformessages(messageseven))
        # first message in another conversation
        self.assertEqual(self.rbg.getresponseformessages(messageeight), '130')
        self.assertEqual(self.rbg.getresponseformessages(messageone),
                         'Hi! :) How are you?')
        # parent messages have not yet been answered
        self.assertFalse(self.rbg.getresponseformessages(messagenine))

suite = unittest.TestLoader().loadTestsFromTestCase(TestResponseBuilderGraph)
unittest.TextTestRunner(verbosity=2).run(suite)
