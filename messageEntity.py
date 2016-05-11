'''
Class to hold messages, done for interop with whatsapp chatbot that relies
on functions of messageEntity class. 
'''

class MessageEntity:
    def __init__(self, sender, text):
        self.sender = sender
        self.text = text

    def getFrom(self):
        return self.sender

    def getBody(self):
        return self.text
