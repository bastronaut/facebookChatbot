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

t = { a : (b, c), b : (d), c: (e, f), d: ()}

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
is_child(G, x, y): tests whether there is an edge from parent vrtx x to child y
add_vertex(G, x): adds the vertex x, if it is not there;
remove_vertex(G, x): removes the vertex x, if it is there;
add_edge(G, x, y): adds the edge from the vertices x to y, if it is not there;
remove_edge(G, x, y): removes the edge from  vertices x to y, if it is there;

'''
from sets import Set


class ResponseBuilderGraph:
    conversations = {}
    sampleconversation = {
        1 : { 'conv_name': 'conv one', 'tree': {
            'a' : ('b', 'c'), 'b' : ('d'), 'c': ('e', 'f'),
            'd': (), 'e': (), 'f': ()}},
        2 : { 'conv_name': 'conv two', 'tree': {
            'a' : ('b', 'c'), 'b' : ('d', 'e'), 'c': ('f'),
            'd': (), 'e': (), 'f': ()}},
        }

    def __init__(self):
        pass

    def is_child(self, conv_id, x, y):
        return y in self.conversations[conv_id][x]

    def add_vertex(self, conv_id, x):
        if x in self.conversations[conv_id]:
            return
        else:
            self.conversations[conv_id][x] = Set([])

    def remove_vertex(self, conv_id, x):
        if x in self.conversations[conv_id]:
            del self.conversations[conv_id][x]

    def add_edge(self, x, y):
        return


if __name__ == "__main__":
    rbg = ResponseBuilderGraph()
    print rbg.sampleconversation


#
#
#
