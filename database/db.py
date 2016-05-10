from pymongo import MongoClient
from sampledata import Sampledata
import pymongo

'''
responsible for getting the questions and responses from DB
a question is: { id: int, text: string, conv_id: int}
a response is : { id: int, text: string, conv_id: int, response_to: [{id: int}, {id: int} ]}
'''

class Db:
    env = 'prod'
    client = MongoClient()
    # client = MongoClient("mongodb://mongodb0.example.net:55888")
    messages = []
    questions = []
    responses = []
    conversations = []
    sampledata = Sampledata()

    def __init__(self):
        if self.env == 'prod':
            self.db = self.client.prod
        else:
            self.db = self.client.test

    def getMessages(self):
        cursor = self.db.messages.find().sort([('conv_id', 1), ('q_nr', 1)])
        for document in cursor:
            self.messages.append(document)
        print 'nr of messages: ', len(self.messages)
        return self.messages

    def getQuestions(self):
        # cursor =  self.db.questions.find().sort({'conv_id': 1, 'q_nr' : 1})
        cursor =  self.db.questions.find().sort([('conv_id', 1), ('q_nr', 1)])
        for document in cursor:
            self.questions.append(document)
        print 'nr of questions: ', len(self.questions)
        return self.questions

    def getResponses(self):
        # cursor = self.db.responses.find().sort({'conv_id': 1, 'r_nr' : 1})
        cursor = self.db.responses.find().sort([('conv_id', 1), ('q_nr', 1)])
        for document in cursor:
            self.responses.append(document)
        print 'nr of responses: ', len(self.responses)
        return self.responses

    def getConversations(self):
        cursor = self.db.convsersations.find()
        for document in cursor:
            self.conversations.append(document)
        return self.conversations

    def _clearMessages(self):
        cursor = self.db.messages.drop()
        return True

    def _clearQuestions(self):
        cursor = self.db.questions.drop()
        return True

    def _clearResponses(self):
        cursor = self.db.responses.drop()
        return True

    def _clearConvsations(self):
        cursor = self.db.conversations.drop()
        return True

    def _clearDb(self):
        try:
            self._clearQuestions()
            self._clearResponses()
            self._clearMessages()
            self._clearConvsations()
            return True
        except Exception, e:
            print e
            return False

    def insertTestData(self):
        testmessages = self.sampledata.getMessages()
        testconvs = self.sampledata.getConversations()
        print 'inserting...'
        self.db.messages.insert(testmessages)
        self.db.conversations.insert(testconvs)

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
