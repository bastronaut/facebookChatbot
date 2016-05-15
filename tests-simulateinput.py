from responseBuilder import ResponseBuilder
from database.db import Db

db = Db()
rb = ResponseBuilder()

print 'starting...'

class SampleMessageProtocolEntity:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = unicode(message)

    def getFrom(self):
        return self.sender

    def getBody(self):
        return self.message


while True:
    incomingmsg = raw_input('Incoming message:')

    db.insertTestIncomingMsg({'message': incomingmsg, 'sender': 'testuser' })
    testmsg = db.getMostRecentTestIncomingMsg()
    msgentity = SampleMessageProtocolEntity(testmsg['sender'], testmsg['message'])
    response = rb.getResponsesForMessage(msgentity)
    if not response:
        print 'no response for input ', incomingmsg, '\n'
