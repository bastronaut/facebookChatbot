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

    # messages in DB are escaped into unicode for security. Incomning msgs
    # are similarly escaped here to ensure a good comparison
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
      return escapedMessage

    def escapeTextPattern(self, input, pattern, replacewith):
        return input.replace(pattern, replacewith)
