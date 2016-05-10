from flask import Flask, request
app = Flask(__name__)
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
    payload = request.get_data()
    print payload, '\n'
    print payload.entry.messaging[0].recipient
    print payload.entry.messaging[0].message.text
    return "ok"



if __name__ == "__main__":
    app.run(debug=True)
