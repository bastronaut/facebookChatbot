from flask import Flask, request
app = Flask(__name__)
from database.db import Db
from responseBuilder import ResponseBuilder

token = 'test'
@app.route('/', methods=['GET'])
def test():
    print 'yolo'
    return 'doei'

@app.route('/fbchatbot/', methods=['GET'])
def verify():
    if request.args.get('hub.verify_token', '') == token:
        print requests.args
        print 'yolo'
        return request.args.get('hub.challenge', '')
    else:
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def webhook():
    payload = request.get_data()
    for sender, message in messenger.messaging_events(payload):
        print "Incoming from %s: %s" % (sender, message)

        response = bot.respond_to(message)

        print "Outgoing to %s: %s" % (sender, response)
        messenger.send_message(FACEBOOK_TOKEN, sender, response)

    return "ok"


if __name__ == "__main__":
    app.run(debug=True)
