from sets import Set
from database.sampledata import Sampledata
from chatbot.responseBuilderGraph import ResponseBuilderGraph
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

    sampleconversations = {}

    def setUp(self):
        self.sampleconversations = {
            1: {'a': set(['b', 'c']), 'b': set('d'), 'c': set(['e', 'f']),
                'd': set(), 'e': set(), 'f': set('g'), 'g': set()},
            2: {'a': set(['c', 'b']), 'b': set(['d', 'e']), 'c': set('f'),
                'd': set(), 'e': set(), 'f': set()},
            3: {'a': set(['c', 'b']), 'b': set([]), 'c': set([])}
            }
        self.rbg = ResponseBuilderGraph()
        self.rbg.setconversations(self.sampleconversations)
        self.sd = Sampledata()
        self.messages = self.sd.getgraphmessages()

    def test_is_child(self):
        self.assertTrue(self.rbg.is_child(1, 'c', 'f'))
        self.assertTrue(self.rbg.is_child(1, 'a', 'b'))
        self.assertTrue(self.rbg.is_child(2, 'b', 'e'))
        self.assertFalse(self.rbg.is_child(1, 'd', 'c'))
        self.assertFalse(self.rbg.is_child(1, 'g', 'f'))
        self.assertFalse(self.rbg.is_child(2, 'x', 'z'))

    def test_add_node(self):
        self.rbg.add_node(1, 'x')
        self.assertTrue(type(self.rbg.conversationtrees[1]['x']) == Set)
        self.rbg.add_node(1, 'a')
        self.assertTrue(self.rbg.conversationtrees[1]['a'] ==
                        set(['c', 'b']))

    def test_remove_node(self):
        remove_result = {'a': set(['c', 'b']), 'b': set(['d']), 'd': set([])}
        self.rbg.remove_node(1, 'c')
        self.assertEqual(self.rbg.conversationtrees[1], remove_result)

        self.rbg.remove_node(1, 'b')
        remove_result = {'a': set(['c', 'b'])}
        self.assertEqual(self.rbg.conversationtrees[1], remove_result)

    def test_remove_edge(self):
        remove_edge_result = {'a': set(['c']), 'c': set(['e', 'f']),
                              'b': set(['d']), 'e': set([]), 'd': set([]),
                              'g': set([]), 'f': set(['g'])}
        self.rbg.remove_edge(1, 'b')
        self.assertEqual(self.rbg.conversationtrees[1], remove_edge_result)

        self.rbg.remove_edge(1, 'DOESNT EXIST')  # result should not change
        self.assertEqual(self.rbg.conversationtrees[1], remove_edge_result)

    def test_add_edge(self):
        add_edge_result = {'a': set(['c', 'b', 'z']), 'b': set([]),
                           'c': set([])}
        self.rbg.add_edge(3, 'a', 'z')
        self.assertEqual(self.rbg.conversationtrees[3], add_edge_result)

        self.rbg.add_edge(3, 'a', 'c')  # already exists, result should not change
        self.assertEqual(self.rbg.conversationtrees[3], add_edge_result)

    def test_buildconversationtrees(self):
        convtreesresult = { 1:
            {123: set([124, 126]), 124: set([125]), 125: set([]),
             126: set([127, 128]), 127: set([]), 128: set([129]), 129: set([])},
            2:
            {130: set([131, 132]), 131: set([133, 134]), 132: set([135]),
             133: set([]), 134: set([]), 135: set([])}}
        self.assertEqual(self.rbg.buildconversationtrees(self.messages), convtreesresult)

    def test_getrootnodes(self):
        rootnodes = {1: 123, 2: 130}
        self.assertEqual(self.rbg.getrootnodes(self.messages), rootnodes)

    def test_getchildnodes(self):
        self.assertEqual(self.rbg.getchildnodes(1, 123), [124, 126])
        self.assertEqual(self.rbg.getchildnodres(1, 999), [])
        self.assertEqual(self.rbg.getchildnodres(2, 132), [135])
        self.assertEqual(self.rbg.getchildnodres(999, 1), [])

suite = unittest.TestLoader().loadTestsFromTestCase(TestResponseBuilderGraph)
unittest.TextTestRunner(verbosity=2).run(suite)
