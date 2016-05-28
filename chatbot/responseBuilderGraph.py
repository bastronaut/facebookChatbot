'''
Building responses is too complex. Better to model a conversation as a tree
graph. Also using pep standard from now on.

Start building all tree graph methods, then probably abstract them away
with chatbot behavior calls. Will use adjacency list for this.
https://en.wikipedia.org/wiki/Adjacency_list
The tree is considered a directed graph (single root node)
Adjacency list is an unordered list of nodes with a set of neighbouring nodes.
tree graph t = { a : (b, c), b : (a), c: (a)}

Tree methods to implement:
is_child(G, x, y): tests whether there is an edge from parent vrtx x to child y
add_vertex(G, x): adds the vertex x, if it is not there;
remove_vertex(G, x): removes the vertex x, if it is there;
add_edge(G, x, y): adds the edge from the vertices x to y, if it is not there;
remove_edge(G, x, y): removes the edge from  vertices x to y, if it is there;


convs = [
    { "conv_id" : 1, "conv_name" : "example chat", "message_tree" : tree t},
    ...
    }

Now, instead of checking in all of the messages whether there is a match,
we simply traverse the tree from their most recent message in each conversation,
check if there is a match only in the child nodes attached to their most recent
message. If so, reply with the child response, and update mostrecentmessage

'''
from sets import Set


class ResponseBuilderGraph:
    conversations = {}

    def __init__(self):
        pass

    def is_child(self, x, y):
        return y in self.conversations[x]

    def add_vertex(self, x):
        if x in self.conversations:
            return
        else:
            self.conversations[x] = Set([])

    def remove_vertex(self, x):
        if x in self.conversations:
            del self.conversations[x]
