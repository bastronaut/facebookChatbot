from flask import Flask, request
app = Flask(__name__)
import json
from database.db import Db
from responseBuilder import ResponseBuilder


token = 'testy'

@app.route('/fbchatbot/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == token:
        print 'yolo'
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'


@app.route('/fbchatbot/', methods=['POST'])
def webhook():
    print 'incoming msg!'
    payload = json.loads(request.get_data())
    messaging = payload["entry"][0]["messaging"]

    for event in messaging:
        if "message" in event and "text" in event["message"]:
            messagesender = event["sender"]
            messagetext = event["message"]["text"]
            print 'sender:', messagesender
            print 'text:', messagetext'

            #TODO:
            # make a messageEntity
            # get response for messageEntity
            # post response
            # do in seperate files
    #print payload, '\n'
    return "ok"




if __name__ == "__main__":
    app.run(debug=True)
