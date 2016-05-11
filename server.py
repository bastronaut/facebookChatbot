from flask import Flask, request
app = Flask(__name__)
import json
from responseBuilder import ResponseBuilder
from messageEntity import MessageEntity
from messageHandler import MessageHandler


responsebuilder = ResponseBuilder()
messageHandler = MessageHandler()
TOKEN = 'testy'

@app.route('/fbchatbot/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == TOKEN:
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
        messageHandler.sendResponse(response, TOKEN)
        print 'sending response!'
    else:
        print 'no response was send.'

    return 'ok'




if __name__ == "__main__":
    app.run(debug=True)
