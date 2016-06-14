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


new conversationstates = {
    m.getFrom() : {
        conv_id : { mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
        conv_id : { mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
        conv_id : { mostrecentinteraction: timestamp, mostrecentquestion: question_nr}},
    m.getFrom() : {
        conv_id : { mostrecentinteraction: timestamp, mostrecentquestion: question_nr},
        conv_id : { mostrecentinteraction: timestamp, mostrecentquestion: question_nr}
        }
}

'''
from sets import Set
from database.sampledata import Sampledata
import re
from datetime import time, tzinfo, datetime, timedelta

class ResponseBuilderGraph:

    def __init__(self):
        self.conversationstates = {}
        # TODO: replace getting test messages with DB messages.
        # insert the correct data struct messages into db first
        self.sd = Sampledata()
        self.messages = self.sd.getgraphmessages()
        self.messagesdict = self.createmessagesdictbykey(self.messages)
        self.conversationtrees = self.buildconversationtrees(self.messages)
        self.RESETMESSAGE = 'chatreset'

    # Create a dict representation of all the stored messages for quick
    # lookup and references. messagedict =
    # { msgkey: { entiremessage}, msgkey2: {entiremessage2}, .. }
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
    # however, it will not delete references to its edges!
    def remove_node(self, conv_id, node):
        if conv_id in self.conversationtrees:
            if node in self.conversationtrees[conv_id]:
                if self.conversationtrees[conv_id][node]:
                    for childnode in self.conversationtrees[conv_id][node]:
                        self.remove_node(conv_id, childnode)
                del self.conversationtrees[conv_id][node]

    # should be called whenever a node is removed. Otherwise, edges are kept
    # in place while the nodes no longer exist
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

    def getrootnodes(self, messages):
        rootnodes = {}
        for message in messages:
            if message['parent'] == 0:
                rootnodes[message['conv_id']] = message['key']
        return rootnodes

    # The child nodes of the most recently asked question of a user are the
    # msgs that warrant a reply. Function returns:
    # conv_id : set(keys of all childnodes eligible for a reply) }
    def getfollowupnodes(self, messageSender):
        followupnodes = {}
        convstate = self.conversationstates.setdefault(messageSender, {})
        for conv_id in convstate:
            childnodes = self.getchildnodes(conv_id, convstate[conv_id]['mostrecentquestion'])
            if childnodes is not None:
                followupnodes[conv_id] = childnodes
            else:
                followupnodes[conv_id] = None
        return followupnodes

    def getchildnodes(self, conv_id, node):
        if conv_id in self.conversationtrees:
            if node in self.conversationtrees[conv_id]:
                return self.conversationtrees[conv_id][node]
        return None

    # Flattens the eligilbe msgs: the list of rootnodes and the list with sets
    #  of followupnodes. Returns [ msgkey, msgkey, msgkey, ...]
    def geteligiblemessages(self, rootnodes, followupnodes):
        eligiblemessages = []
        for node in rootnodes:
            eligiblemessages.append(rootnodes[node])
        for childnodesets in followupnodes:
            for node in followupnodes[childnodesets]:
                eligiblemessages.append(node)
        return eligiblemessages

    # In order to find whether the incoming message warrants a response,
    # we compare it only to messages that are eligible for a response.
    # PROBLEMATIC: because of the way RE \b works, this has some problems when
    # the sentence ends/begins with special characters. Example:
    # r'\b' + 'Not great...' + r'\b' will not match 'xx Not great... xx'
    # need to test impact of stripping characters before matching, but is nasty
    # workaround
    def getmessagematches(self, incomingmessage, eligiblemessages, messagedict):
        matches = []
        for msgkey in eligiblemessages:
            loweredmessage = messagedict[msgkey]['qtext'].lower()
            if (re.search(r'\b' + loweredmessage + r'\b', incomingmessage)
                         or loweredmessage == incomingmessage):
                matches.append(msgkey)
        return matches

    def updateconversationstate(self, messageSender, conv_id, msgkey):
        self.conversationstates.setdefault(messageSender, {})
        self.conversationstates[messageSender].setdefault(conv_id, {})
        self.conversationstates[messageSender][conv_id] = {'mostrecentinteraction': datetime.utcnow(),
                                                           'mostrecentquestion': msgkey }

    def reinitialize(self, messageSender):
        if messageSender in self.conversationstates:
            self.conversationstates[messageSender] = {}
        return

    def getresponseformessages(self, message):
        returnResponses = []
        messageSender = message.getFrom()
        try:
            messagetext = message.getBody().lower()
        except Exception, e:
            print 'Fail getBody, will not work for Media messages:', e
            return returnResponses

        if messagetext == self.RESETMESSAGE:
            self.reinitialize(messageSender)
            return False

        rootnodes = self.getrootnodes(self.messages)
        followupnodes = self.getfollowupnodes(messageSender)
        eligiblemessages = self.geteligiblemessages(rootnodes, followupnodes)

        escapedmessage = message.replaceEscapedCharacters(messagetext)
        matches = self.getmessagematches(escapedmessage, eligiblemessages, self.messagesdict)

        if matches:
            for match in matches:
                self.updateconversationstate(messageSender, self.messagesdict[match]['conv_id'], match)
                returnResponses.append({'responseText' : self.messagesdict[match]['rtext']})
        return returnResponses

if __name__ == "__main__":
    rbg = ResponseBuilderGraph()
    rbg.buildconversationtrees(rbg.messages)
    sampleconvstates = rbg.sd.getsampleconversationstates()
    rbg.getfollowupnodes(sampleconvstates['hank'])
    rbg.geteligiblemessages(rbg.getrootnodes(rbg.messages), rbg.getfollowupnodes(sampleconvstates))
