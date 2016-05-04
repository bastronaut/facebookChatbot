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

if __name__ == "__main__":
    app.run(debug=True)
