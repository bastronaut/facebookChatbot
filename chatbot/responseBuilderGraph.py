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
we simply traverse the tree from their mostrecent message in each conversation,
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

    def add_edge(self, conv_id, node, edge):
        if edge in self.conversations[conv_id]['tree'][node]:
            return
        else:
            self.conversations[conv_id]['tree'][node].add(edge)

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
        self.conversations = conversations

    def getmatches(self, message):
        return

    def getfirstmessageids(self):
        for conversation in self.conversations:
            return  # TODO

    def getresponseformessages(self, message):
        # find which message ids warrant a response
        #   all the first message ids in a tree
        #   the edges connected to the node of their most recent messages
        # check whether one of these messages matches the incoming message
        # if so, return the response
        return

# TODO:
# the python script will not be responsible for inserting and maintaining
# the tree. the nodejs script will be inserting and updating the treeself.
# therefore, we have to add it to the node api. we have to store it in such a way
# that it can easily be parsed and serialized into a tree
# possible options: https://docs.mongodb.com/manual/applications/data-models-tree-structures/
# probably the child reference model:
# https://docs.mongodb.com/manual/tutorial/model-tree-structures-with-child-references/

if __name__ == "__main__":
    rbg = ResponseBuilderGraph()
    print '####################\nThe start is:\n', rbg.conversations[1]['tree']
