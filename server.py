from flask import Flask, request
app = Flask(__name__)
import json
import chatbot.messageEntity
from chatbot.messageHandler import MessageHandler
import credentials

messageHandler = MessageHandler()
VERIFYTOKEN = credentials.VERIFYTOKEN
AUTHTOKEN = credentials.AUTHTOKEN
testmode = True

@app.route('/fbchatbot/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == VERIFYTOKEN:
        print 'verify token sent'
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'


@app.route('/fbchatbot/', methods=['POST'])
def webhook():
    print 'incoming msg!'
    payload = json.loads(request.get_data())

    response = messageHandler.buildResponseForRequest(payload)

    if response:
        if testmode:
            print 'Mock sending response for:', response, '\n..returning..'
            return 'ok'

        ### temporary messy multiplechoice test
        if response['responsetext'] == 'multiplechoice!':
            messageHandler.testMultipleChoiceResponse(response, AUTHTOKEN)

        print 'sending response!'
        messageHandler.sendResponse(response, AUTHTOKEN)

    else:
        print 'no response was send.'
    return 'ok'


if __name__ == "__main__":
    app.run(debug=True)
