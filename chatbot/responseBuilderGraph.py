'''
WORK IN PROGRESS, this class will soon phase out responseBuilder class

Conversations are modeled as a directed (tree) graph. Each message
question/response is a node in the graph. An edge between the nodes in a
conversation are follow-up messages. In order to reach a certain node in the
graph, all of its parent nodes must have been 'asked' by the user.

Now, instead of checking in all of the messages whether there is a match,
we simply traverse the tree from their mostrecent message in each conversation,
check if there is a match only in the child nodes attached to their most recent
message. If so, reply with the child's response, and update mostrecentmessage

t =
        a
     /      \
    b         c
    |       /   \
    d       e   f
                |
                g
t = { a : (b, c), b : (d), c: (e, f), d: set()}

sampleconversationtree = {
            1: {123: set([124, 126]), 124: set([125]), 125: set([]),
                126: set([127, 128]), 127: set([]), 128: set([129]), 129: set([])},
            2: {130: set([131, 132]), 131: set([133, 134]), 132: set([135]),
                133: set([]), 134: set([]), 135: set([])}
            }

Tree methods to implement:
is_child(G, x, y): tests whether there is an edge from parent node x to child y
add_node(G, x): adds the node x, if it is not there;
remove_node(G, x): removes the node x, if it is there;
add_edge(G, x, y): adds the edge from the vertices x to y, if it is not there;
remove_edge(G, x, y): removes the edge from  vertices x to y, if it is there;

'''
from sets import Set
from database.sampledata import Sampledata


class ResponseBuilderGraph:

    def __init__(self):
        self.conversationstates = {}
        self.sd = Sampledata()
        self.messages = self.sd.getgraphmessages()
        self.messagesdict = self.createmessagesdictbykey(self.messages)
        self.conversationtrees = self.buildconversationtrees(self.messages)
        self.rootnotes = self.getrootnodes(self.messages)
        self.resetmsg = 'chatreset'

    # Create a dict representation of all the stored messages for quick
    # lookup and references. messagedict =
    # { key: { entiremessage}, key2: {entiremessage} }
    def createmessagesdictbykey(self, messages):
        messagedict = {}
        for message in messages:
            messagedict[message['key']] = message
        return messagedict

    def buildconversationtrees(self, messages):
        conversationtrees = {}
        for message in messages:
            conversationtrees.setdefault(message['conv_id'], {})
            conversationtrees[message['conv_id']][message['key']] = set(message['children'])
        return conversationtrees

    def is_child(self, conv_id, parent, child):
        try:
            return child in self.conversationtrees[conv_id][parent]
        except Exception:
            return False

    def add_node(self, conv_id, node_id):
        if node_id in self.conversationtrees[conv_id]:
            return
        else:
            self.conversationtrees[conv_id][node_id] = Set([])

    # will recursively delete a node and all its child components
    # however, it will not delete references to itself as edges!
    def remove_node(self, conv_id, node):
        if conv_id in self.conversationtrees:
            if node in self.conversationtrees[conv_id]:
                if self.conversationtrees[conv_id][node]:
                    for childnode in self.conversationtrees[conv_id][node]:
                        self.remove_node(conv_id, childnode)
                del self.conversationtrees[conv_id][node]

    # should be called whenever a node is removed. Otherwise, edges
    def remove_edge(self, conv_id, edge):
        for node in self.conversationtrees[conv_id]:
            if edge in self.conversationtrees[conv_id][node]:
                self.conversationtrees[conv_id][node].remove(edge)
                break

    def add_edge(self, conv_id, node, edge):
        if edge in self.conversationtrees[conv_id][node]:
            return
        else:
            self.conversationtrees[conv_id][node].add(edge)

    def setconversations(self, conversations):
        self.conversationtrees = conversations

    def getmatches(self, message):
        return

    def getrootnodes(self, messages):
        rootnodes = {}
        for message in messages:
            if message['parent'] == 0:
                rootnodes[message['conv_id']] = message['key']
        return rootnodes

    # The child nodes of the most recently asked question of a user are the
    # messages that are eligible for a reply. Function returns:
    # { conv_id : set(keys of all childnodes eligible for a reply) }
    def getfollowupnodes(self, convstate):
        followupnodes = {}
        for conv_id in convstate:
            followupnodes[conv_id] = self.getchildnodes(conv_id, convstate[conv_id]['mostrecentquestion'])
        return followupnodes

    def getchildnodes(self, conv_id, node):
        if conv_id in self.conversationtrees:
            if node in self.conversationtrees[conv_id]:
                return self.conversationtrees[conv_id][node]
        return None

    def replaceEscapedCharacters(self, message):
      escapedMessage = self.escapeTextPattern(message, '$', '&#36;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '<', '&#60')
      escapedMessage = self.escapeTextPattern(escapedMessage, '>', '&#62;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '\'', '&#39;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '"', '&#34;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '\\', '&#92;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '/', '&#47;')
      escapedMessage = self.escapeTextPattern(escapedMessage, '[', '&#91;')
      escapedMessage = self.escapeTextPattern(escapedMessage, ':', '&#58;')
      print '\n## the escaped msg:', escapedMessage
      return escapedMessage

    def escapeTextPattern(self, input, pattern, replacewith):
        return input.replace(pattern, replacewith)

    # in order to find whether the incoming message warrants a response,
    # we compare it only to the messages that are eligible to receive a
    # response rather than the whole set of messages
    def getmessagematches(self, incomingmessage, eligiblemessages, messagedict):
        matches = []
        for msgkey in eligiblemessages:
            loweredmessage = messagedict[msgkey]['qtext'].lower()
            if (re.search(r'\b' + loweredmessage + r'\b', incomingmessage)
                         or loweredmessage == incomingmessage):
                matches.append(msgkey)
        return matches

    def getresponseformessages(self, message):
        returnResponses = []
        messageSender = message.getFrom()
        try:
            message = message.getBody().lower()
        except Exception, e:
            logging.info(['Fail getBody, probably different msg Type (e.g. media). Error: ', e])
            return returnResponses

        if message == self.resetmsg:
            self.reinitialize(messageSender)
            return False

        message = self.replaceEscapedCharacters(message)

        rootnodes = self.getrootnodes(self.messages)
        followupnodes = self.getfollowupnodes(self.conversationstates)


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
    rbg.buildconversationtrees(rbg.messages)
