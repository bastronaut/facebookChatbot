'''
Building responses is too complex. Better to model a conversation as a tree
graph. Also try using pep standard from now on.

Start building all tree graph methods, then probably abstract them away
with chatbot behavior calls. Will use adjacency list for this.
https://en.wikipedia.org/wiki/Adjacency_list
The tree is considered a directed graph (single root node)
Adjacency list is an unordered list of nodes with a set of neighbouring nodes.
tree graph t:
        a
     /      \
    b         c
    |       /   \
    d       e   f
                |
                g
t = { a : (b, c), b : (d), c: (e, f), d: set()}

data struct:
convs = {
    conv_id : { conv_name: 'name', tree: t },
    conv_id : { conv_name: 'name', tree: t },
    ...
    }

Stored as document per conv id in db:
convs = [
        {conv_id : { conv_name: 'name', tree: t}},
        {conv_id : { conv_name: 'name', tree: t}},
        ...
        ]

Now, instead of checking in all of the messages whether there is a match,
we simply traverse the tree from their most recent message in each conversation,
check if there is a match only in the child nodes attached to their most recent
message. If so, reply with the child response, and update mostrecentmessage

Tree methods to implement:
is_child(G, x, y): tests whether there is an edge from parent node x to child y
add_node(G, x): adds the node x, if it is not there;
remove_node(G, x): removes the node x, if it is there;
add_edge(G, x, y): adds the edge from the vertices x to y, if it is not there;
remove_edge(G, x, y): removes the edge from  vertices x to y, if it is there;

'''
from sets import Set


class ResponseBuilderGraph:
    # conversations = {}
    conversations = {
        1: {'conv_name': 'conv one', 'tree': {
            'a': set(['b', 'c']), 'b': set('d'), 'c': set(['e', 'f']),
            'd': set(), 'e': set(), 'f': set('g'), 'g': set()}},
        2: {'conv_name': 'conv two', 'tree': {
            'a': set(['b', 'c']), 'b': set(['d', 'e']), 'c': set('f'),
            'd': set(), 'e': set(), 'f': set()}},
        }

    def __init__(self):
        pass

    def is_child(self, conv_id, parent, child):
        try:
            return child in self.conversations[conv_id]['tree'][parent]
        except Exception:
            return False

    def add_node(self, conv_id, node_id):
        if node_id in self.conversations[conv_id]['tree']:
            # print self.conversations[conv_id]['tree'][node_id]
            return
        else:
            self.conversations[conv_id]['tree'][node_id] = Set([])

    # will recursively delete a node and all its child components
    def remove_node(self, conv_id, node):
        if node in self.conversations[conv_id]['tree']:
            if self.conversations[conv_id]['tree'][node]:
                for childnode in self.conversations[conv_id]['tree'][node]:
                    self.remove_node(conv_id, childnode)
            del self.conversations[conv_id]['tree'][node]

    def remove_edge(self, conv_id, edge):
        for node in self.conversations[conv_id]['tree']:
            if edge in self.conversations[conv_id]['tree'][node]:
                self.conversations[conv_id]['tree'][node].remove(edge)
                break

    def add_edge(self, x, y):
        return

    def resetconvs(self):
        conversationsbackup = {
            1: {'conv_name': 'conv one', 'tree': {
                'a': set(['b', 'c']), 'b': set('d'), 'c': set(['e', 'f']),
                'd': set(), 'e': set(), 'f': set('g'), 'g': set()}},
            2: {'conv_name': 'conv two', 'tree': {
                'a': set(['b', 'c']), 'b': set(['d', 'e']), 'c': set('f'),
                'd': set(), 'e': set(), 'f': set()}},
            }
        print 'resetting convs..'
        self.conversations = conversationsbackup

    def setconversations(self, conversations):
        print 'setting conversations to:\n', conversations[1]['tree']
        self.conversations = conversations


if __name__ == "__main__":
    rbg = ResponseBuilderGraph()
    print '####################\nThe start is:\n', rbg.conversations[1]['tree']
    # print rbg.is_child(1, 'a', 'g')
    # rbg.remove_node(1, 'c')
    rbg.remove_edge(1, 'b')
    print '####################\nThe end is:\n', rbg.conversations[1]['tree']
    # rbg.remove_node(1, 'b')
    # print '####################\nThe end is:\n', rbg.conversations[1]['tree']
    # rbg.resetconvs()
