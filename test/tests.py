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

    sampleconversations = {
        1: {'conv_name': 'conv one', 'tree': {
            'a': set(['b', 'c']), 'b': set('d'), 'c': set(['e', 'f']),
            'd': set(), 'e': set(), 'f': set('g'), 'g': set()}},
        2: {'conv_name': 'conv two', 'tree': {
            'a': set(['c', 'b']), 'b': set(['d', 'e']), 'c': set('f'),
            'd': set(), 'e': set(), 'f': set()}},
        3: {'conv_name': 'conv two', 'tree': {
            'a': set(['c', 'b']), 'b': set([]), 'c': set([])}}
        }

    def setUp(self):
        print '\n\nrunning setup\n\n#' 
        self.rbg = ResponseBuilderGraph()
        self.rbg.setconversations(self.sampleconversations)

    def test_is_child(self):
        self.assertTrue(self.rbg.is_child(1, 'c', 'f'))
        self.assertTrue(self.rbg.is_child(1, 'a', 'b'))
        self.assertTrue(self.rbg.is_child(2, 'b', 'e'))
        self.assertFalse(self.rbg.is_child(1, 'd', 'c'))
        self.assertFalse(self.rbg.is_child(1, 'g', 'f'))
        self.assertFalse(self.rbg.is_child(2, 'x', 'z'))

    def test_add_node(self):
        self.rbg.add_node(1, 'x')
        self.assertTrue(type(self.rbg.conversations[1]['tree']['x']) == Set)
        self.rbg.add_node(1, 'a')
        self.assertTrue(self.rbg.conversations[1]['tree']['a'] ==
                        set(['c', 'b']))

    def test_remove_node(self):
        self.rbg.remove_node(1, 'c')
        remove_result = {'a': set(['c', 'b']), 'b': set(['d']), 'd': set([])}
        self.assertEqual(self.rbg.conversations[1]['tree'], remove_result)

        self.rbg.remove_node(1, 'b')
        remove_result = {'a': set(['c', 'b'])}
        self.assertEqual(self.rbg.conversations[1]['tree'], remove_result)

    def test_remove_edge(self):
        print 'before:##############\n\n', self.rbg.conversations[1]['tree']
        self.rbg.remove_edge(1, 'b')
        print 'after:##############\n\n', self.rbg.conversations[1]['tree']
        remove_edge_result = {'a': set(['c']), 'c': set(['e', 'f']),
                              'b': set(['d']), 'e': set([]), 'd': set([]),
                              'g': set([]), 'f': set(['g'])}
        print '\n', remove_edge_result
        self.assertEqual(self.rbg.conversations[1]['tree'], remove_edge_result)
        # self.rbg.remove_edge(1, 'DOESNT EXIST')
        # self.assertEqual(self.rbg.conversations[1]['tree'], remove_edge_result)



suite = unittest.TestLoader().loadTestsFromTestCase(TestResponseBuilderGraph)
unittest.TextTestRunner(verbosity=2).run(suite)
