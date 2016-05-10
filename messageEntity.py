class MessageEntity:
    def __init__(self, sender, message):
        self.sender = sender
        self.message = unicode(message)

    def getFrom(self):
        return self.sender

    def getBody(self):
        return self.message
