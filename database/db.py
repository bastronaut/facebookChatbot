from pymongo import MongoClient
from sampledata import Sampledata
import pymongo

class Db:
    env = 'prod'
    client = MongoClient()
    # client = MongoClient("mongodb://mongodb0.example.net:55888")
    sampledata = Sampledata()

    def __init__(self):
        if self.env == 'prod':
            self.db = self.client.prod
        else:
            self.db = self.client.test

    def getMessages(self):
        messages = []
        cursor = self.db.messages.find().sort([('conv_id', 1), ('q_nr', 1)])
        for document in cursor:
            messages.append(document)
        print 'nr of messages: ', len(messages)
        return messages

    def getConversations(self):
        conversations = []
        cursor = self.db.convsersations.find()
        for document in cursor:
            conversations.append(document)
        return conversations

    def _clearMessages(self):
        cursor = self.db.messages.drop()
        return True

    def _clearConvsations(self):
        cursor = self.db.conversations.drop()
        return True

    def _clearDb(self):
        try:
            self._clearMessages()
            self._clearConvsations()
            return True
        except Exception, e:
            print e
            return False

    def insertTestData(self):
        testmessages = self.sampledata.getMessages()
        testconvs = self.sampledata.getConversations()
        graphmsg = self.sampledata.getgraphmessages()
        print 'inserting...'
        self.db.messages.insert(testmessages)
        self.db.conversations.insert(testconvs)
        self.db.graphdata.insert(graphmsg)

    def resetDBToTestState(self):
        print 'resetting...'
        self._clearDb()
        self.insertTestData()

    def clearTestIncomingMsg(self):
        self.db.testincomingmsgs.drop()

    # simulating test incoming msgs, mongodb stores strings as unicode
    def insertTestIncomingMsg(self, msg):
        self.db.testincomingmsgs.insert(msg)

    def getMostRecentTestIncomingMsg(self):
        result = list(self.db.testincomingmsgs.find().sort([('$natural', pymongo.DESCENDING)]).limit(1))
        return result[0]

    def storeIncomingMsg(self, messagesender, messagetext, timestamp):
        self.db.incomingmessages.insert({'sender': messagesender, 'messagetext' : messagetext, 'timestamp' : timestamp})

    def storeOutgoingMsg(self, messagesender, responsetext, timestamp):
        self.db.outgoingmessages.insert({'sender': messagesender, 'responsetext' : responsetext, 'timestamp' : timestamp})
